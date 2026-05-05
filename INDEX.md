# KB Index

Searchable index of all KB entries. Newest entries on top.

**Search tips**

```bash
rg -i "<term>" INDEX.md               # search titles, descriptions, tags, and paths
rg -i "<term>" kb/                    # full-text search across entries
rg -n "^tags:.*\b<tag>\b" kb/        # filter by tag
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
| kb0001 | kb | How this KB framework works | Personal knowledge base framework conventions, entry layout, tags, and maintenance workflow. | meta, conventions, kb-system | [kb/meta/kb0001-kb-framework/kb0001-kb-framework.md](kb/meta/kb0001-kb-framework/kb0001-kb-framework.md) |
