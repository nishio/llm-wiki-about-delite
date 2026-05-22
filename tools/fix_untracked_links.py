#!/usr/bin/env python3
"""Fix Markdown links in the 7 files that were manually moved (not via the
first refactor pass).  These files were originally at concepts/X.md and
moved to wiki/concepts/utagawa/X.md, so all bare '[Y](Y.md)' style links
need to be resolved against the OLD location and rewritten to the NEW
relative location.

Same logic as refactor_concepts.py's link rewriter, but specialized for
just these 7 files.
"""

import os
import re
from pathlib import Path

ROOT = Path("/Users/nishio/delite")

# These were moved by hand after the first run.
FILES = [
    "wiki/concepts/utagawa/副日記.md",
    "wiki/concepts/utagawa/一日一文.md",
    "wiki/concepts/utagawa/一選万集.md",
    "wiki/concepts/utagawa/書了.md",
    "wiki/concepts/utagawa/整輪.md",
    "wiki/concepts/utagawa/『希哲日記』.md",
    "wiki/concepts/utagawa/日記準備整輪.md",
]

# Build a reverse lookup: stem -> new path (relative to ROOT).
NEW_BY_STEM = {}
for d in ["wiki/concepts/utagawa", "wiki/concepts", "wiki/people", "wiki/meta"]:
    for f in (ROOT / d).glob("*.md"):
        NEW_BY_STEM[f.stem] = str(f.relative_to(ROOT))

LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')

def rewrite_link(file_new_path: str, text: str, link: str) -> str:
    if link.startswith(("http://", "https://", "mailto:", "ftp://", "//")):
        return f"[{text}]({link})"
    if link.startswith("#"):
        return f"[{text}]({link})"

    if "#" in link:
        link_path, anchor = link.split("#", 1)
        anchor = "#" + anchor
    else:
        link_path = link
        anchor = ""

    if not link_path:
        return f"[{text}]({link})"

    # These files were originally in concepts/, so resolve against concepts/.
    OLD_DIR = "concepts"
    try:
        old_target = os.path.normpath(os.path.join(OLD_DIR, link_path))
        old_target = old_target.replace(os.sep, "/")
    except Exception:
        return f"[{text}]({link})"

    # If the path refers to a file outside concepts/ (e.g. ../sources/X.md),
    # the new target keeps its original path.
    # If it points to concepts/X.md, look up the new home.
    if old_target.startswith("concepts/"):
        stem = Path(old_target).stem
        new_target = NEW_BY_STEM.get(stem)
        if new_target is None:
            # Unknown / broken link, keep as-is
            return f"[{text}]({link})"
    else:
        new_target = old_target

    file_new_dir = Path(file_new_path).parent
    new_rel = os.path.relpath(new_target, file_new_dir).replace(os.sep, "/")
    return f"[{text}]({new_rel}{anchor})"

updated = 0
for fp in FILES:
    full = ROOT / fp
    if not full.exists():
        print(f"missing: {fp}")
        continue
    content = full.read_text(encoding="utf-8")
    new_content = LINK_RE.sub(
        lambda m: rewrite_link(fp, m.group(1), m.group(2)),
        content,
    )
    if new_content != content:
        full.write_text(new_content, encoding="utf-8")
        updated += 1
        print(f"updated: {fp}")

print(f"Total updated: {updated}")
