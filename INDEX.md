# KB Index

Searchable index of all KB entries. Newest entries on top.

## Search Tips

```bash
rg -i "<term>" INDEX.md               # search titles, descriptions, tags, and paths
rg -i "<term>" kb/                    # full-text search across entries
rg -n "^tags:.*\b<tag>\b" kb/        # filter by tag
rg "^scripts:" kb/                    # find entries that include scripts
ls kb/                                # list topics
ls kb/{topic}/                        # list entries in a topic
ls kb/{topic}/kbNNNN-short-title/data/ # list support files for an entry
```

See [README.md](README.md) for usage, [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance, and [AGENTS.md](AGENTS.md) for agent guidance.

To regenerate this index from frontmatter: `python3 tools/generate_index.py`

## Entries

| ID | Type | Title | Description | Tags | Path |
| --- | --- | --- | --- | --- | --- |
| kb0003 | kb | Link inbox | Starter inbox for saving, deduplicating, and annotating useful URLs before they become KB entries. | links, research, kb-system, maintenance | [kb/links/kb0003-link-inbox/kb0003-link-inbox.md](kb/links/kb0003-link-inbox/kb0003-link-inbox.md) |
| kb0002 | kb | Agent skills for KB maintenance | Agent-agnostic skills for creating, searching, auditing, and preserving this knowledge base. | meta, conventions, kb-system, agents, skills | [kb/meta/kb0002-agent-skills/kb0002-agent-skills.md](kb/meta/kb0002-agent-skills/kb0002-agent-skills.md) |
| kb0001 | kb | How this KB framework works | Personal knowledge base framework conventions, entry layout, tags, and maintenance workflow. | meta, conventions, kb-system | [kb/meta/kb0001-kb-framework/kb0001-kb-framework.md](kb/meta/kb0001-kb-framework/kb0001-kb-framework.md) |
