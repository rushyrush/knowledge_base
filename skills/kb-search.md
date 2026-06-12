# KB Search Skill

## Purpose

Search and answer questions from this knowledge base with concise citations.

Use this skill when the user asks to find KB entries, answer from KB content, cite KB IDs, inspect topics or tags, locate scripts, or check freshness.

## Workflow

1. Search `INDEX.md` for titles, descriptions, tags, and paths:

   ```bash
   rg -i "{term}" INDEX.md
   ```

2. Search full KB content:

   ```bash
   rg -i "{term}" kb/
   ```

3. Read the most relevant primary notes before answering. Prefer:

   ```text
   kb/{topic}/kbNNNN-short-title/kbNNNN-short-title.md
   ```

4. Read support files under `data/` when they materially affect the answer.
5. Answer concisely, then cite supporting hits by KB ID and relative Markdown link.

## Useful Filters

```bash
rg -n "^tags:.*\b{tag}\b" kb/          # filter by tag
rg "^scripts:" kb/                      # find entries that include scripts
rg "^last_verified:" kb/ | sort -t: -k3 # find stale entries
ls kb/                                  # list topics
ls kb/{topic}/                          # list entries in a topic
```

## Answer Format

Default to:

```markdown
<concise answer>

Sources: [kbNNNN](relative/path/to/kbNNNN-slug.md), [kbNNNN](relative/path/to/kbNNNN-slug.md)
```

When useful, mention the entry type, support files under `data/`, and `last_verified` or `updated` if freshness matters.

## Handling Gaps

- If no KB entry answers the question, say that the KB has no matching entry and mention the closest hits if any.
- If entries conflict, cite both and explain the discrepancy briefly.
- If an entry looks stale, call out `last_verified` or `updated` and avoid overstating certainty.
- If the user asks for something operational, prefer runbooks and script entries over general reference entries.
