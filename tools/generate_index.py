#!/usr/bin/env python3
"""Regenerate INDEX.md from KB frontmatter.

Discovers entries that use the hybrid layout:

    kb/{topic}/kbNNNN-short-title/kbNNNN-short-title.md

The index is sorted by ID descending, newest on top.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_DIR = REPO_ROOT / "kb"
INDEX_PATH = REPO_ROOT / "INDEX.md"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
ENTRY_DIR_RE = re.compile(r"^kb\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(text: str) -> dict:
    """Minimal YAML frontmatter parser for this framework's flat metadata."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            value = [item.strip() for item in value[1:-1].split(",") if item.strip()]
        frontmatter[key] = value
    return frontmatter


def discover_entry_files() -> list[Path]:
    """Return primary note files using the hybrid entry directory convention."""
    if not KB_DIR.exists():
        return []

    entry_files: list[Path] = []
    for topic_dir in sorted(path for path in KB_DIR.iterdir() if path.is_dir()):
        for entry_dir in sorted(path for path in topic_dir.iterdir() if path.is_dir()):
            if not ENTRY_DIR_RE.match(entry_dir.name):
                print(f"  WARN: skipping non-entry directory {entry_dir.relative_to(REPO_ROOT)}", file=sys.stderr)
                continue

            expected_note = entry_dir / f"{entry_dir.name}.md"
            if expected_note.exists():
                entry_files.append(expected_note)
                continue

            notes = sorted(path for path in entry_dir.glob("kb*.md") if path.is_file())
            if len(notes) == 1:
                print(
                    f"  WARN: using {notes[0].relative_to(REPO_ROOT)}; expected {expected_note.name}",
                    file=sys.stderr,
                )
                entry_files.append(notes[0])
            elif notes:
                print(f"  WARN: multiple candidate notes in {entry_dir.relative_to(REPO_ROOT)}", file=sys.stderr)
            else:
                print(f"  WARN: no primary note in {entry_dir.relative_to(REPO_ROOT)}", file=sys.stderr)

    return entry_files


def collect_entries() -> list[dict]:
    entries = []
    for note_path in discover_entry_files():
        frontmatter = parse_frontmatter(note_path.read_text(encoding="utf-8"))
        if not frontmatter.get("id"):
            print(f"  WARN: no id in {note_path.relative_to(REPO_ROOT)}", file=sys.stderr)
            continue

        tags = frontmatter.get("tags", [])
        if isinstance(tags, str):
            tags = [tag.strip() for tag in tags.strip("[]").split(",") if tag.strip()]

        rel_path = note_path.relative_to(REPO_ROOT)
        entries.append({
            "id": frontmatter["id"],
            "type": frontmatter.get("type", "kb"),
            "title": frontmatter.get("title", ""),
            "description": frontmatter.get("description", ""),
            "tags": ", ".join(tags),
            "path": str(rel_path),
            "status": frontmatter.get("status", "active"),
        })

    entries.sort(key=lambda entry: entry["id"], reverse=True)
    return entries


def table_text(entries: list[dict]) -> str:
    header = """# KB Index

Searchable index of all KB entries. Newest entries on top.

**Search tips**

```bash
rg -i "<term>" INDEX.md               # search titles, descriptions, tags, and paths
rg -i "<term>" kb/                    # full-text search across entries
rg -n "^tags:.*\\b<tag>\\b" kb/        # filter by tag
rg "^scripts:" kb/                    # find entries that include scripts
ls kb/                                # list topics
ls kb/{topic}/                        # list entries in a topic
ls kb/{topic}/kbNNNN-short-title/data/ # list support files for an entry
```

See [README.md](README.md) for usage, [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance, and [AGENTS.md](AGENTS.md) for the agent workflow.

To regenerate this index from frontmatter: `python3 tools/generate_index.py`

## Entries

| ID | Type | Title | Description | Tags | Path |
|----|------|-------|-------------|------|------|
"""

    lines = [header]
    for entry in entries:
        title = entry["title"]
        if entry["status"] == "deprecated":
            title = f"[deprecated] {title}"
        elif entry["status"] == "archived":
            title = f"[archived] {title}"
        lines.append(
            f"| {entry['id']} | {entry['type']} | {title} | {entry['description']} "
            f"| {entry['tags']} | [{entry['path']}]({entry['path']}) |\n"
        )
    return "".join(lines)


def main() -> None:
    entries = collect_entries()
    INDEX_PATH.write_text(table_text(entries), encoding="utf-8")
    print(f"INDEX.md regenerated with {len(entries)} entries.")


if __name__ == "__main__":
    main()
