---
id: kb0001
title: How this KB framework works
description: Personal knowledge base framework conventions, entry layout, tags, and maintenance workflow.
tags: [meta, conventions, kb-system]
aliases: [KB framework overview]
type: kb
status: active
last_verified: 2026-06-12
data_gaps: []
created: 2026-05-02
updated: 2026-06-26
---

## Context

This repository is a starter framework for a personal knowledge base. It is designed for Markdown editors, Obsidian, command-line search, and agents that can add or update structured entries.

Each entry has a permanent `kbNNNN` ID, a readable slug, YAML frontmatter, and a body shaped for the type of information being captured. Entries can also include nearby entry-local artifacts in a `data/` directory.

The full conventions live in [README.md](../../../README.md) for humans, [CONTRIBUTING.md](../../../CONTRIBUTING.md) for contributors, and [AGENTS.md](../../../AGENTS.md) for agents. This entry is the worked example.

## Two kinds of knowledge

The repository deliberately separates curated knowledge from source knowledge so people and agents never confuse them:

- **`kb/` (curated knowledge)** -- authored, summarized entries with stable `kbNNNN` IDs, indexed in [INDEX.md](../../../INDEX.md). This is *what you know*: conventions, how-tos, runbooks, decisions.
- **`corpus/` (source knowledge)** -- complete or near-complete upstream documentation preserved verbatim, indexed in [CORPUS_INDEX.md](../../../CORPUS_INDEX.md), with no `kbNNNN` IDs. This is *what you have*: full product docs, API references, imported Markdown trees.

A *corpus* is a collection of source material gathered for retrieval and reference. To give an agent the full Helm documentation, import it as a corpus at `corpus/products/helm/` instead of compressing it into one KB entry; a curated entry can then link to that corpus for deep detail. See [corpus/README.md](../../../corpus/README.md) for the corpus workflow.

When answering questions, search curated KB first, then the corpus: if a KB entry references a corpus, follow it; if only the corpus matches, answer from it and note that it is source documentation rather than curated guidance.

## Layout

Every entry is a directory with a unique stem and one primary Markdown note inside:

```text
kb/{topic}/kbNNNN-short-title/
├── kbNNNN-short-title.md
└── data/                    # optional support files for this entry
```

The `data/` directory is optional. Use it for source material, raw notes, transcripts, pasted docs, scripts, configs, inventories, diagrams, screenshots, exported logs, generated outputs, or anything else that belongs with the entry.

The hybrid `kbNNNN-short-title` stem keeps each note unique in Obsidian's quick switcher, backlinks, and graph view, while the directory keeps support files local. The repo opens cleanly as an Obsidian vault.

## Steps

To add a new entry by hand:

1. Open [INDEX.md](../../../INDEX.md), find the largest `kbNNNN`, add 1, and zero-pad to four digits.
2. Pick or create a topic folder under `kb/` (lowercase kebab-case).
3. Pick a short kebab-case slug from the title (3-4 keywords is plenty), e.g. `ssh-key-rotation`.
4. Create the directory `kb/{topic}/kbNNNN-{slug}/`.
5. Copy [_template/kb.md](../../../_template/kb.md) into that directory and rename it to `kbNNNN-{slug}.md` (the file stem must match the directory name).
6. Fill the frontmatter:
   - `id` matches the ID prefix, e.g. `kb0042`.
   - `title`: short noun phrase or imperative, <=80 chars.
   - `description`: one sentence, <=120 chars; front-load key nouns.
   - `tags`: 3-7 lowercase kebab-case tokens; check [tags.md](../../../tags.md) first.
   - `aliases`: optional Obsidian-friendly alternative names, or `[]`.
   - `type`: `kb`, `runbook`, or `script`.
   - `scripts`: optional list of script paths relative to the entry directory, e.g. `[data/rotate-key.sh]`.
   - `status`: `active` for new entries.
   - `last_verified`: today's date.
   - `data_gaps`: list of claims you could not verify, or `[]`.
   - `created` / `updated`: today's date.
7. Write the body. For runbooks use Symptoms -> Diagnosis -> Resolution -> Verification -> Rollback. For scripts use Context -> Usage -> Parameters -> Example Output -> Gotchas.
8. If this KB includes entry-local artifacts, create `data/` inside the entry directory and place them there. Scripts must have a shebang, be `chmod +x`, and include a usage comment.
9. Regenerate the index: `python3 tools/generate_index.py`
10. Validate: `python3 tools/validate.py`

To have an agent do all of this, just say **"turn this into a KB"** and paste the source.

## Gotchas

- **IDs are permanent.** Never renumber or reuse. If an entry is obsolete, set `status: deprecated`; do not delete the file.
- **Stem must match.** The note filename stem must equal the entry directory name (`kbNNNN-short-title`). The ID, directory stem, note filename stem, and `INDEX.md` row all have to agree.
- **Cross-links use full paths.** Same-topic peers: `[Title](../kbNNNN-slug/kbNNNN-slug.md)`. Cross-topic peers: `[Title](../../topic/kbNNNN-slug/kbNNNN-slug.md)`.
- **Tag hygiene matters.** Check [tags.md](../../../tags.md) for canonical tags before inventing new ones.
- **Description is the primary search text.** Index searches mostly hit this field, so front-load nouns and avoid filler like "How to..." or "A guide for...".
- **No secrets.** Redact tokens, credentials, private URLs, customer data, and anything that should not be shared.
- **Entry-local artifacts go in `data/`.** When a KB has source material, raw notes, transcripts, pasted docs, scripts, configs, inventories, diagrams, screenshots, exported logs, generated outputs, or other files, place them in `kbNNNN-slug/data/`. No ID prefix on filenames inside `data/`; the parent directory provides the KB context. Scripts must have a shebang, be `chmod +x`, and include a usage comment. List them in the `scripts:` frontmatter field.
- **Agent skills live at repo root.** Root-level `skills/*.md` files are global reusable workflows for maintaining KB quality, not support files for one entry.
- **Verify regularly.** Bump `last_verified` whenever you confirm a KB is still accurate.

## Searching

```bash
# Metadata search via the index
rg -i "{term}" INDEX.md

# Full-text search across all entries
rg -i "{term}" kb/

# Filter by tag
rg -n "^tags:.*\\b{tag}\\b" kb/

# Find stale entries
rg "^last_verified:" kb/ | sort -t: -k3
```

## Obsidian

- Open the repo root as an Obsidian vault.
- The `kbNNNN-short-title.md` stems keep each note distinct in the quick switcher and graph.
- Add `aliases:` in frontmatter if you want a friendlier display name (e.g. `aliases: [SSH key rotation]`).

## References

- [README.md](../../../README.md) -- human-facing usage guide
- [CONTRIBUTING.md](../../../CONTRIBUTING.md) -- contribution checklist
- [AGENTS.md](../../../AGENTS.md) -- agent workflow and hard rules
- [Agent skills for KB maintenance](../kb0002-agent-skills/kb0002-agent-skills.md) -- reusable agent skills catalog
- [_template/kb.md](../../../_template/kb.md) -- entry scaffold
- [INDEX.md](../../../INDEX.md) -- searchable generated index
- [tags.md](../../../tags.md) -- starter tag taxonomy
