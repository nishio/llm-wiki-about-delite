#!/usr/bin/env python3
"""Walk all wiki/, sources/, and the top-level *.md and report any
local Markdown link whose target file does not exist on disk.
"""

import os
import re
from pathlib import Path

ROOT = Path("/Users/nishio/delite")
LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')

targets = []
for top in ["index.md", "CLAUDE.md", "log.md", "init.txt", "llm-wiki.md"]:
    p = ROOT / top
    if p.exists() and p.suffix == ".md":
        targets.append(p)
for d in ["wiki", "sources"]:
    for p in (ROOT / d).rglob("*.md"):
        targets.append(p)

broken = []
for p in targets:
    content = p.read_text(encoding="utf-8")
    for m in LINK_RE.finditer(content):
        link = m.group(2)
        if link.startswith(("http://", "https://", "mailto:", "ftp://", "//", "#")):
            continue
        # Strip anchor
        link_path = link.split("#", 1)[0]
        if not link_path:
            continue
        # Resolve relative to this file's directory
        target = (p.parent / link_path).resolve()
        if not target.exists():
            broken.append((str(p.relative_to(ROOT)), link, str(target.relative_to(ROOT)) if target.is_relative_to(ROOT) else str(target)))

print(f"Files checked: {len(targets)}")
print(f"Broken links : {len(broken)}")
for src, link, resolved in broken[:50]:
    print(f"  {src} -> {link!r}  (resolved: {resolved})")
if len(broken) > 50:
    print(f"  ... and {len(broken)-50} more")
