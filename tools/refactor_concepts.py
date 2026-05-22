#!/usr/bin/env python3
"""Refactor concepts/ → wiki/{concepts/utagawa, concepts, people, meta}/ .

Plan (per user instruction in second.txt):
  /wiki/concepts/         -- 概念全般
  /wiki/concepts/utagawa/ -- 宇田川氏の作った概念
  /wiki/people/           -- 人物プロフィール
  /wiki/meta/             -- メタページ

All Markdown links of the form [text](path.md) are rewritten so they
keep pointing at the same file after relocation.
"""

import os
import re
import subprocess
from pathlib import Path

ROOT = Path("/Users/nishio/delite")
CONCEPTS = ROOT / "concepts"

all_concepts = sorted([f.stem for f in CONCEPTS.glob("*.md")])

# ----- Classification -----
# 久住哲・zatsma・nyarla等のユーザー側用語、外部の Cosense 用語、メタデータ書式
OTHERS = {
    "認知パースペクティブ", "景間距離", "エンティティとしての投稿", "輪郭名",
    "立体アウトライナー", "SNSとしてのデライト",
    "複合的階層構造SNSとしてのデライトの紹介",
    "名づけずに語る", "デライトにコミットするコストとそれへの対策",
    "デライト用語ではない", "のような位置づけ",
    "ブラケティング", "輪符をブラケティング",
    "接触元",
}
PEOPLE = {"デライト開発者", "ジェンドリン"}
META = {"先行概念マッピング"}

UTAGAWA = set(all_concepts) - OTHERS - PEOPLE - META

print(f"Total concept files: {len(all_concepts)}")
print(f"  utagawa : {len(UTAGAWA)}")
print(f"  others  : {len(OTHERS)}")
print(f"  people  : {len(PEOPLE)}")
print(f"  meta    : {len(META)}")

unknown_in_others = OTHERS - set(all_concepts)
unknown_in_people = PEOPLE - set(all_concepts)
unknown_in_meta = META - set(all_concepts)
if unknown_in_others or unknown_in_people or unknown_in_meta:
    print(f"WARN: missing files: {unknown_in_others | unknown_in_people | unknown_in_meta}")

# ----- Build move map -----
moves = {}  # old (rel str) -> new (rel str)
for stem in UTAGAWA:
    moves[f"concepts/{stem}.md"] = f"wiki/concepts/utagawa/{stem}.md"
for stem in OTHERS:
    moves[f"concepts/{stem}.md"] = f"wiki/concepts/{stem}.md"
for stem in PEOPLE:
    moves[f"concepts/{stem}.md"] = f"wiki/people/{stem}.md"
for stem in META:
    moves[f"concepts/{stem}.md"] = f"wiki/meta/{stem}.md"

assert len(moves) == len(all_concepts), f"moves={len(moves)} files={len(all_concepts)}"

# ----- Create directories -----
for d in ["wiki/concepts/utagawa", "wiki/concepts", "wiki/people", "wiki/meta"]:
    (ROOT / d).mkdir(parents=True, exist_ok=True)

# ----- git mv -----
for old, new in moves.items():
    res = subprocess.run(
        ["git", "-C", str(ROOT), "mv", old, new],
        capture_output=True, text=True
    )
    if res.returncode != 0:
        print(f"git mv failed: {old} -> {new}: {res.stderr}")

print("Files moved.")

# ----- Build files-to-process list -----
files_to_process = list(moves.values())
for top in ["index.md", "CLAUDE.md", "log.md"]:
    if (ROOT / top).exists():
        files_to_process.append(top)
for sf in (ROOT / "sources").glob("*.md"):
    files_to_process.append(str(sf.relative_to(ROOT)))

LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')

def old_path_for(new_path_str: str) -> str:
    for old, new in moves.items():
        if new == new_path_str:
            return old
    return new_path_str  # Not moved

def rewrite_link(file_new_path: str, text: str, link: str) -> str:
    # External / anchor-only / scheme links
    if link.startswith(("http://", "https://", "mailto:", "ftp://", "//")):
        return f"[{text}]({link})"
    if link.startswith("#"):
        return f"[{text}]({link})"

    file_old_path = old_path_for(file_new_path)
    file_old_dir = Path(file_old_path).parent

    if "#" in link:
        link_path, anchor = link.split("#", 1)
        anchor = "#" + anchor
    else:
        link_path = link
        anchor = ""

    if not link_path:
        return f"[{text}]({link})"

    try:
        old_target = os.path.normpath(str(file_old_dir / link_path))
        old_target = old_target.replace(os.sep, "/")
    except Exception:
        return f"[{text}]({link})"

    new_target = moves.get(old_target, old_target)

    file_new_dir = Path(file_new_path).parent
    new_rel = os.path.relpath(new_target, file_new_dir).replace(os.sep, "/")

    return f"[{text}]({new_rel}{anchor})"

updated = 0
for fp in files_to_process:
    full_path = ROOT / fp
    if not full_path.exists():
        continue
    content = full_path.read_text(encoding="utf-8")
    new_content = LINK_RE.sub(
        lambda m: rewrite_link(fp, m.group(1), m.group(2)),
        content
    )
    if new_content != content:
        full_path.write_text(new_content, encoding="utf-8")
        updated += 1

print(f"Updated link references in {updated} files.")
print("Done.")
