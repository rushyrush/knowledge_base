---
id: kb0001
title: How this KB framework works
description: Personal knowledge base framework conventions, entry layout, tags, and maintenance workflow.
tags: [meta, conventions, kb-system]
aliases: [KB framework overview]
type: kb
status: active
last_verified: 2026-05-02
data_gaps: []
created: 2026-05-02
updated: 2026-05-02
---

# How this KB framework works

## Context

This repository is a starter framework for a personal knowledge base. It is designed for Markdown editors, Obsidian, command-line search, and AI agents that can add or update structured entries.

Each entry has a permanent `kbNNNN` ID, a readable slug, YAML frontmatter, and a body shaped for the type of information being captured. Entries can also include nearby support files in a `data/` directory.

## Layout

Use one directory per entry:

```text
kb/{topic}/kbNNNN-short-title/
├── kbNNNN-short-title.md
└── data/
```

The `data/` directory is optional. Use it for scripts, configs, screenshots, exports, or other files that belong with the entry.

## Steps

To add a new entry by hand:

1. Open `INDEX.md` and find the largest `kbNNNN` ID.
2. Add 1 to allocate the next ID, preserving four digits.
3. Pick or create a lowercase kebab-case topic folder under `kb/`.
4. Create a directory named `kbNNNN-short-title`.
5. Copy `_template/kb.md` into that directory and rename it to `kbNNNN-short-title.md`.
6. Fill the frontmatter and delete unused template sections.
7. Run `python3 tools/generate_index.py`.
8. Run `python3 tools/validate.py`.

## Gotchas

- IDs are permanent. Do not reuse or renumber them.
- Keep note filenames unique and readable so Obsidian quick switcher, backlinks, and graph views are useful.
- Prefer broad reusable tags from `tags.md` before adding new tags.
- Do not save secrets, private URLs, customer data, access tokens, or credentials in the KB.
- If an entry has support files, keep them under that entry's `data/` directory.

## References

- [README.md](../../../README.md) -- human-facing usage guide
- [CONTRIBUTING.md](../../../CONTRIBUTING.md) -- contribution checklist
- [AGENTS.md](../../../AGENTS.md) -- agent workflow and hard rules
- [_template/kb.md](../../../_template/kb.md) -- entry scaffold
- [INDEX.md](../../../INDEX.md) -- searchable generated index
- [tags.md](../../../tags.md) -- starter tag taxonomy
