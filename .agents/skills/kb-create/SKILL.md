---
name: kb-create
description: Create, update, and deprecate KB entries while preserving framework invariants. Use when turning source material into a KB entry, updating an existing KB, or marking an entry obsolete.
---

# KB Create Skill

## Purpose

Create, update, and deprecate entries in this knowledge base while preserving the framework invariants documented in `AGENTS.md`.

Use this skill when the user asks to turn source material into a KB entry, update an existing KB, or mark an entry obsolete.

## Source Of Truth

Before creating, updating, or deprecating a KB entry, read `AGENTS.md` at the repository root. Treat it as canonical if this skill and `AGENTS.md` disagree.

## Workflow

1. Determine the entry type: `kb`, `runbook`, or `script`. Ask only if the type is genuinely ambiguous.
2. Choose an existing topic folder under `kb/` when one fits. Ask only when the topic is genuinely ambiguous.
3. Allocate the next ID from `INDEX.md`, then confirm it is unused with `rg "^id: kbNNNN$" kb/`.
4. Choose a short lowercase kebab-case slug and use the hybrid stem `kbNNNN-short-title` for both directory and Markdown filename.
5. Create `kb/{topic}/kbNNNN-short-title/kbNNNN-short-title.md` from `_template/kb.md`.
6. If the entry includes source material, raw notes, transcripts, pasted docs, scripts, configs, inventories, diagrams, screenshots, exported logs, generated outputs, or other accompanying files, place them under `data/` beside the note.
7. Fill frontmatter exactly: `id`, `title`, `description`, `tags`, `aliases`, `type`, optional `scripts`, `status`, `last_verified`, `data_gaps`, `created`, and `updated`.
8. Check `tags.md` before inventing tags. Prefer 3-7 existing lowercase kebab-case tags.
9. Write a concise structured body, not a raw paste.
10. Regenerate `INDEX.md` with `python3 tools/generate_index.py`.
11. Verify the ID, path, frontmatter, and index row all agree.
12. Run `python3 tools/validate.py`.

## Body Shapes

- `kb`: Context, Steps or Details, Gotchas, References.
- `runbook`: Symptoms, Diagnosis, Resolution, Verification, Rollback.
- `script`: Context, Usage, Parameters, Example Output, Gotchas, References.

For script entries, every script must have a shebang, be executable, include a usage comment block, and be listed in `scripts:` using a path relative to the entry directory.

## Updating Existing Entries

- Never change the `id`.
- Bump `updated:` to today's date.
- Bump `last_verified:` only when the content was re-verified as accurate.
- Regenerate `INDEX.md` if title, description, tags, status, or path changed.
- If moving an entry, keep the same ID and rename the directory and note file so their stems still match.

## Deprecating Entries

- Never delete a KB file or directory.
- Set `status: deprecated`.
- Add a short note near the top explaining why and linking to any replacement.
- Regenerate `INDEX.md`.

## Completion

Report the created or updated path and the verification performed.
