# Contributing

This framework is meant to stay simple: one Markdown note per KB entry, stable IDs, useful tags, and no private data.

## Before You Add An Entry

- Check `INDEX.md` and `kb/` to avoid duplicating an existing entry.
- Pick the next unused `kbNNNN` ID.
- Pick a lowercase kebab-case topic folder.
- Check `tags.md` before inventing a tag.
- Remove or redact secrets, credentials, private URLs, customer data, and other non-shareable details.

## Create The Entry

Use the hybrid layout:

```text
kb/{topic}/kbNNNN-short-title/
├── kbNNNN-short-title.md
└── data/
```

The `data/` directory is optional. Use it for entry-local artifacts that belong with the KB, such as source material, raw notes, transcripts, pasted docs, scripts, configs, inventories, diagrams, screenshots, exported logs, generated outputs, or other supporting files.

Files inside `data/` inherit context from the parent `kbNNNN-short-title` directory, so use descriptive filenames without repeating the KB ID prefix.

Copy `_template/kb.md` into the entry directory and rename the copy to match the directory stem.

## Write The Entry

- Use `type: kb` for references, how-tos, explainers, and conventions.
- Use `type: runbook` for operational response steps.
- Use `type: script` when executable files are the main deliverable.
- Keep the title short and the description search-friendly.
- Prefer concise steps, gotchas, and references over raw pasted notes.
- Link related entries by ID, such as `kb0001`.

## Scripts And Support Files

If an entry includes support files:

- Put source material, raw notes, transcripts, pasted docs, scripts, configs, inventories, diagrams, screenshots, exported logs, generated outputs, and other entry-local artifacts under that entry's `data/` directory.
- For scripts, add a shebang such as `#!/usr/bin/env bash`, include a short usage comment near the top, and make the script executable.
- List script paths in frontmatter with paths relative to the entry directory.

Example:

```yaml
scripts: [data/example.sh]
```

Root-level `skills/*.md` files are different: they are global agent skills for maintaining KB quality, not support files for a single KB entry.

## KB vs Corpus

This repo separates two kinds of knowledge:

- **`kb/`** holds curated entries you author: summaries, how-tos, runbooks, conventions. They get stable `kbNNNN` IDs and appear in `INDEX.md`.
- **`corpus/`** holds full source documentation you import: complete product docs, API references, upstream Markdown trees. Collections get no `kbNNNN` ID and appear in `CORPUS_INDEX.md` instead.

Use a corpus when the value is in keeping the **complete source** searchable (for example, all of the Helm docs). Use a KB entry when the value is in your **distilled** guidance. A KB entry may reference a corpus for deep detail.

To add a corpus:

1. Create `corpus/{category}/{slug}/` (usually `corpus/products/{slug}/`).
2. Copy `corpus/_template/corpus.yaml` into it and fill in every field.
3. Import the docs under `docs/`, preferring Markdown or text, and redact anything private.
4. Add a row to `CORPUS_INDEX.md`.

See [corpus/README.md](corpus/README.md) for the full workflow.

## Validate Before Sharing

Run these commands from the repository root:

```bash
python3 tools/generate_index.py
python3 tools/validate.py
```

Before publishing or sharing a copy, also search for private terms that should not leave your machine.
