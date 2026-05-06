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

The `data/` directory is optional. Use it for files that belong with the entry, such as scripts, configs, diagrams, exported logs, or screenshots.

Copy `_template/kb.md` into the entry directory and rename the copy to match the directory stem.

## Write The Entry

- Keep the title short and the description search-friendly.
- Prefer concise steps, gotchas, and references over raw pasted notes.
- For operational notes (incident response, troubleshooting, diagnosis), use: Context, Symptoms, Diagnosis, Resolution, Verification, Rollback, References. The body shape communicates intent — the type is still `kb`.
- Link related entries by ID, such as `kb0001`.

## Scripts And Support Files

If an entry includes scripts:

- Put scripts under that entry's `data/` directory.
- Add a shebang, such as `#!/usr/bin/env bash`.
- Include a short usage comment near the top.
- Make the script executable.
- List script paths in frontmatter with paths relative to the entry directory.

Example:

```yaml
scripts: [data/example.sh]
```

## Validate Before Sharing

Run these commands from the repository root:

```bash
python3 tools/generate_index.py
python3 tools/validate.py
```

Before publishing or sharing a copy, also search for private terms that should not leave your machine.