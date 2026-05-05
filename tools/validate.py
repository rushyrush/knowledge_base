#!/usr/bin/env python3
"""Validate the KB repo for structural integrity.

Checks:
1. Every hybrid entry directory has exactly one matching primary note.
2. Every primary note has valid frontmatter and required fields.
3. Every entry on disk has a row in INDEX.md.
4. Every row in INDEX.md has a corresponding file on disk.
5. Frontmatter IDs match directory and filename ID prefixes.
6. Scripts listed in frontmatter exist and are executable.
7. Tags are present in tags.md (warns on unknown tags).
8. IDs are unique.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_DIR = REPO_ROOT / "kb"
INDEX_PATH = REPO_ROOT / "INDEX.md"
TAGS_PATH = REPO_ROOT / "tags.md"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
ENTRY_DIR_RE = re.compile(r"^(kb\d{4})-[a-z0-9]+(?:-[a-z0-9]+)*$")

REQUIRED_FIELDS = [
    "id",
    "title",
    "description",
    "tags",
    "type",
    "status",
    "last_verified",
    "data_gaps",
    "created",
    "updated",
]

VALID_TYPES = {"kb", "runbook", "script"}
VALID_STATUSES = {"active", "draft", "deprecated", "archived"}

errors: list[str] = []
warnings: list[str] = []


def error(message: str) -> None:
    errors.append(message)
    print(f"  ERROR: {message}", file=sys.stderr)


def warn(message: str) -> None:
    warnings.append(message)
    print(f"  WARN:  {message}", file=sys.stderr)


def parse_frontmatter(text: str) -> dict:
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


def as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [item.strip() for item in str(value).strip("[]").split(",") if item.strip()]


def load_canonical_tags() -> set[str]:
    if not TAGS_PATH.exists():
        warn("tags.md not found; skipping tag validation.")
        return set()

    tags = set()
    for line in TAGS_PATH.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^- `([^`]+)`", line)
        if match:
            tags.add(match.group(1))
    return tags


def load_index_ids() -> dict[str, str]:
    """Return {id: path} from INDEX.md table rows."""
    if not INDEX_PATH.exists():
        error("INDEX.md not found.")
        return {}

    ids: dict[str, str] = {}
    for line in INDEX_PATH.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\| (kb\d{4}) \|", line)
        if not match:
            continue
        kb_id = match.group(1)
        path_match = re.search(r"\[([^\]]+)\]\([^\)]+\)", line)
        ids[kb_id] = path_match.group(1) if path_match else ""
    return ids


def discover_entry_dirs() -> list[Path]:
    if not KB_DIR.exists():
        error("kb/ directory not found.")
        return []

    entry_dirs: list[Path] = []
    for topic_dir in sorted(path for path in KB_DIR.iterdir() if path.is_dir()):
        for entry_dir in sorted(path for path in topic_dir.iterdir() if path.is_dir()):
            if ENTRY_DIR_RE.match(entry_dir.name):
                entry_dirs.append(entry_dir)
            else:
                warn(f"{entry_dir.relative_to(REPO_ROOT)}: directory does not match kbNNNN-short-title.")
    return entry_dirs


def validate_entry(entry_dir: Path, canonical_tags: set[str], index_ids: dict[str, str], disk_ids: dict[str, Path]) -> None:
    rel_dir = entry_dir.relative_to(REPO_ROOT)
    dir_match = ENTRY_DIR_RE.match(entry_dir.name)
    if not dir_match:
        return

    dir_id = dir_match.group(1)
    expected_note = entry_dir / f"{entry_dir.name}.md"
    primary_notes = sorted(path for path in entry_dir.glob("kb*.md") if path.is_file())

    if not expected_note.exists():
        error(f"{rel_dir}: expected primary note '{expected_note.name}'.")
        return

    extra_notes = [path for path in primary_notes if path != expected_note]
    if extra_notes:
        extras = ", ".join(str(path.relative_to(REPO_ROOT)) for path in extra_notes)
        error(f"{rel_dir}: multiple primary note candidates: {extras}.")

    note_rel = expected_note.relative_to(REPO_ROOT)
    frontmatter = parse_frontmatter(expected_note.read_text(encoding="utf-8"))
    if not frontmatter:
        error(f"{note_rel}: no frontmatter found.")
        return

    kb_id = frontmatter.get("id", "")
    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            error(f"{note_rel}: missing required field '{field}'.")

    if kb_id and not re.match(r"^kb\d{4}$", kb_id):
        error(f"{note_rel}: id '{kb_id}' does not match kbNNNN pattern.")

    if kb_id and kb_id != dir_id:
        error(f"{note_rel}: id '{kb_id}' does not match directory ID '{dir_id}'.")

    file_id = expected_note.stem.split("-", 1)[0]
    if kb_id and kb_id != file_id:
        error(f"{note_rel}: id '{kb_id}' does not match filename ID '{file_id}'.")

    if expected_note.stem != entry_dir.name:
        error(f"{note_rel}: note filename stem must match entry directory name '{entry_dir.name}'.")

    if kb_id in disk_ids:
        error(f"{note_rel}: duplicate id '{kb_id}' (also at {disk_ids[kb_id]}).")
    elif kb_id:
        disk_ids[kb_id] = note_rel

    if kb_id and kb_id not in index_ids:
        error(f"{note_rel}: id '{kb_id}' not found in INDEX.md.")
    elif kb_id and index_ids.get(kb_id) != str(note_rel):
        error(f"{note_rel}: INDEX.md path for '{kb_id}' is '{index_ids.get(kb_id)}'.")

    entry_type = frontmatter.get("type", "")
    if entry_type and entry_type not in VALID_TYPES:
        error(f"{note_rel}: invalid type '{entry_type}'. Must be kb|runbook|script.")

    status = frontmatter.get("status", "")
    if status and status not in VALID_STATUSES:
        error(f"{note_rel}: invalid status '{status}'. Must be active|draft|deprecated|archived.")

    tags = as_list(frontmatter.get("tags", []))
    if len(tags) < 3 or len(tags) > 7:
        warn(f"{note_rel}: expected 3-7 tags; found {len(tags)}.")
    if canonical_tags:
        for tag in tags:
            if tag not in canonical_tags:
                warn(f"{note_rel}: tag '{tag}' not in tags.md.")

    scripts = as_list(frontmatter.get("scripts", []))
    for script in scripts:
        script_path = entry_dir / script
        if Path(script).is_absolute() or ".." in Path(script).parts:
            error(f"{note_rel}: script '{script}' must be relative to the entry directory.")
            continue
        if not script_path.exists():
            error(f"{note_rel}: script '{script}' listed in frontmatter but not found.")
        elif not os.access(script_path, os.X_OK):
            error(f"{note_rel}: script '{script}' is not executable.")


def main() -> None:
    print("Validating KB repository...\n")

    canonical_tags = load_canonical_tags()
    index_ids = load_index_ids()
    disk_ids: dict[str, Path] = {}

    for entry_dir in discover_entry_dirs():
        validate_entry(entry_dir, canonical_tags, index_ids, disk_ids)

    for index_id, index_path in index_ids.items():
        if index_id not in disk_ids:
            error(f"INDEX.md references '{index_id}' at '{index_path}' but no entry note found on disk.")

    print(f"\n{'=' * 50}")
    print(f"  {len(disk_ids)} KB entries found on disk")
    print(f"  {len(index_ids)} entries in INDEX.md")
    print(f"  {len(errors)} errors, {len(warnings)} warnings")
    print(f"{'=' * 50}")

    if errors:
        print("\nFailed.", file=sys.stderr)
        sys.exit(1)

    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
