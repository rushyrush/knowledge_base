---
name: kb-search
description: Search and answer from KB content with citations, drawing on curated KB entries and full source documentation in the corpus. Use when finding KB entries, citing KB IDs, inspecting topics or tags, or pulling in source docs.
---

# KB Search Skill

## Purpose

Search and answer questions from this knowledge base with concise citations, drawing on both curated KB entries and full source documentation in the corpus.

Use this skill when the user asks to find KB entries, answer from KB content, cite KB IDs, inspect topics or tags, locate scripts, check freshness, or pull in full product/source documentation.

## Knowledge sources

- **`kb/` (curated)** -- authored entries indexed in `INDEX.md`. Cite by `kbNNNN` ID.
- **`corpus/` (source docs)** -- full documentation collections indexed in `CORPUS_INDEX.md`. Cite by collection and file path.

## Workflow

1. Search curated KB first -- `INDEX.md` for titles, descriptions, tags, and paths:

   ```bash
   rg -i "{term}" INDEX.md
   ```

2. Search full KB content:

   ```bash
   rg -i "{term}" kb/
   ```

3. Search source documentation -- the corpus discovery index and full text:

   ```bash
   rg -i "{term}" CORPUS_INDEX.md
   rg -i "{term}" corpus/
   ```

4. Read the most relevant primary notes before answering. Prefer:

   ```text
   kb/{topic}/kbNNNN-short-title/kbNNNN-short-title.md
   ```

5. Read support files under `data/` when they materially affect the answer.
6. If a KB entry references a corpus, follow that reference and read the relevant `corpus/` docs for deeper detail.
7. Answer concisely, then cite supporting hits: KB entries by ID and relative Markdown link, corpus material by collection and file path.

## Resolution rules

- Prefer curated KB for local conventions and decisions.
- If no KB entry matches but corpus material does, answer from the corpus and state clearly that it is source documentation, not curated KB guidance.
- If KB guidance and corpus docs conflict, prefer the KB for local conventions and cite the corpus for upstream behavior.

## Useful Filters

```bash
rg -n "^tags:.*\b{tag}\b" kb/          # filter by tag
rg "^scripts:" kb/                      # find entries that include scripts
rg "^last_verified:" kb/ | sort -t: -k3 # find stale entries
ls kb/                                  # list topics
ls kb/{topic}/                          # list entries in a topic
rg -i "{term}" CORPUS_INDEX.md          # discover a source-doc collection
ls corpus/products/                     # list product corpora
rg -i "{term}" corpus/products/{slug}/  # search within one collection
```

## Answer Format

Default to:

```markdown
<concise answer>

Sources: [kbNNNN](relative/path/to/kbNNNN-slug.md), corpus/products/{slug}/docs/<file>.md
```

When useful, mention the entry type, support files under `data/`, and `last_verified` or `updated` if freshness matters. When citing corpus material, make clear it is source documentation rather than curated KB guidance.

## Handling Gaps

- If neither the KB nor the corpus answers the question, say so and mention the closest hits if any.
- If a KB entry and corpus docs conflict, cite both, prefer the KB for local conventions, and use the corpus for upstream behavior.
- If an entry looks stale, call out `last_verified` or `updated` and avoid overstating certainty.
- If the user asks for something operational, prefer runbooks and script entries over general reference entries.
- If the user needs exhaustive product detail, search the corpus and cite the specific files rather than summarizing from memory.
