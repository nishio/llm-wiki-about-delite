#!/usr/bin/env python3
"""Normalize broken links left over after the refactor.

After moving concepts/X.md to wiki/concepts/utagawa/X.md (etc.), any
ORIGINAL '[Y](Y.md)' that pointed to a non-existent Y.md got rewritten to
'../../../concepts/Y.md' (the old relative path) since the script could
not find Y.md in the moves table.

These were red links to begin with.  Normalize them so the path is
simple and short, treating them as same-directory red links again.
"""

import os
import re
from pathlib import Path

ROOT = Path("/Users/nishio/delite")
LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')

# Build set of EXISTING files (anywhere in the wiki tree).
existing_paths = set()
for d in ["wiki", "sources"]:
    for f in (ROOT / d).rglob("*.md"):
        existing_paths.add(str(f.relative_to(ROOT)).replace(os.sep, "/"))
existing_stems = {Path(p).stem: p for p in existing_paths}

targets_to_scan = []
for d in ["wiki", "sources"]:
    for p in (ROOT / d).rglob("*.md"):
        targets_to_scan.append(p)

def rewrite_link(file_path: Path, text: str, link: str) -> str:
    if link.startswith(("http://", "https://", "mailto:", "ftp://", "//", "#")):
        return f"[{text}]({link})"
    if "#" in link:
        link_body, anchor = link.split("#", 1)
        anchor = "#" + anchor
    else:
        link_body = link
        anchor = ""
    if not link_body:
        return f"[{text}]({link})"

    # Resolve against the file's directory.
    try:
        target_abs = (file_path.parent / link_body).resolve()
        target_rel = str(target_abs.relative_to(ROOT.resolve())).replace(os.sep, "/")
    except (ValueError, OSError):
        return f"[{text}]({link})"

    if target_rel in existing_paths:
        return f"[{text}]({link})"  # already correct
    # Broken.  Try to map to an existing file by stem.
    stem = Path(target_rel).stem
    if stem in existing_stems:
        new_target = existing_stems[stem]
        new_rel = os.path.relpath(new_target, file_path.parent).replace(os.sep, "/")
        return f"[{text}]({new_rel}{anchor})"
    # Still broken — collapse to a same-directory red link with just the
    # bare filename.
    bare = Path(link_body).name
    return f"[{text}]({bare}{anchor})"

updated = 0
for p in targets_to_scan:
    content = p.read_text(encoding="utf-8")
    new_content = LINK_RE.sub(
        lambda m: rewrite_link(p, m.group(1), m.group(2)),
        content,
    )
    if new_content != content:
        p.write_text(new_content, encoding="utf-8")
        updated += 1
        print(f"normalized: {p.relative_to(ROOT)}")

print(f"Total updated: {updated}")
