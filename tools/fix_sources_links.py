#!/usr/bin/env python3
"""Re-apply move-aware link rewriting to sources/*.md ONLY.

This is run after restoring sources/ from HEAD (the pre-refactor state).
It uses the actual current filesystem layout to determine where each old
concepts/X.md file now lives, and rewrites links accordingly.

Links to raw/, tools/, etc. are PRESERVED untouched.
"""

import os
import re
from pathlib import Path

ROOT = Path("/Users/nishio/delite")
LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')

# Discover where each concept file currently lives.
# stem -> new relative path
stem_to_newpath = {}
for d in ["wiki/concepts/utagawa", "wiki/concepts", "wiki/people", "wiki/meta"]:
    for f in (ROOT / d).glob("*.md"):
        stem_to_newpath[f.stem] = str(f.relative_to(ROOT)).replace(os.sep, "/")

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

    # Resolve link against file's OLD directory (i.e., its current sources/ dir).
    try:
        old_target_abs = (file_path.parent / link_body).resolve()
        old_target_rel = str(old_target_abs.relative_to(ROOT.resolve())).replace(os.sep, "/")
    except (ValueError, OSError):
        return f"[{text}]({link})"

    # Only rewrite if the link points into concepts/ (the old structure).
    if not old_target_rel.startswith("concepts/"):
        # raw/, tools/, sources/, anything else — leave alone
        return f"[{text}]({link})"

    # concepts/SOMETHING.md or concepts/ (directory ref)
    rest = old_target_rel[len("concepts/"):]
    if not rest:
        # concepts/ directory reference — point to wiki/concepts/
        new_target = "wiki/concepts"
    elif rest.endswith(".md"):
        stem = Path(rest).stem
        if stem in stem_to_newpath:
            new_target = stem_to_newpath[stem]
        else:
            # Unknown / red link.  Map to wiki/concepts/X.md as a placeholder.
            new_target = f"wiki/concepts/{rest}"
    else:
        new_target = old_target_rel  # Unknown shape, leave alone

    file_dir = file_path.parent
    new_rel = os.path.relpath(new_target, file_dir).replace(os.sep, "/")
    return f"[{text}]({new_rel}{anchor})"

updated = 0
for sf in (ROOT / "sources").glob("*.md"):
    content = sf.read_text(encoding="utf-8")
    new_content = LINK_RE.sub(
        lambda m: rewrite_link(sf, m.group(1), m.group(2)),
        content,
    )
    if new_content != content:
        sf.write_text(new_content, encoding="utf-8")
        updated += 1
        print(f"updated: {sf.relative_to(ROOT)}")

print(f"Total updated: {updated}")
