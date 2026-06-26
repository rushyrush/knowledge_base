# Personal KB Framework

A shareable starter framework for building a personal knowledge base with plain Markdown, stable IDs, searchable metadata, optional support files, link capture, and agent-friendly conventions.

It works as a normal folder of Markdown files, an Obsidian vault, and a command-line searchable reference library. It is designed for humans and agents to share and expand together: humans contribute context and judgment, while agents help turn raw source material into durable KB entries.

## Quickstart

1. Copy or clone this repository for your own KB.
2. Open it in your editor or in Obsidian as a vault.
3. Read the example entry at [kb/meta/kb0001-kb-framework/kb0001-kb-framework.md](kb/meta/kb0001-kb-framework/kb0001-kb-framework.md).
4. Create your first entry from [_template/kb.md](_template/kb.md), or give an agent source material and ask it to **"turn this into a KB"**. Good source material includes files, shell-session notes, chat transcripts, links, or text pasted directly into agent chat.
5. Regenerate the index:

   ```bash
   python3 tools/generate_index.py
   ```

6. Validate the repo:

   ```bash
   python3 tools/validate.py
   ```

## Layout

```text
KB/
├── README.md                       # how to use the framework
├── CONTRIBUTING.md                 # lightweight contribution checklist
├── AGENTS.md                       # canonical instructions agents follow
├── CLAUDE.md                       # symlink compatibility alias to AGENTS.md
├── INDEX.md                        # searchable index of curated KB entries
├── CORPUS_INDEX.md                 # discovery index of source-doc collections
├── .agents/skills/                 # native agent skills for KB maintenance (one SKILL.md per skill)
├── _template/kb.md                 # copy + rename when adding a new entry
├── tags.md                         # canonical tag taxonomy
├── tools/                          # index generator and validator
├── kb/
│   ├── meta/                       # KBs about the KB itself
│   └── {topic}/                    # one folder per topic, lowercase kebab-case
│       └── kbNNNN-short-title/     # every KB is a directory with a unique stem
│           ├── kbNNNN-short-title.md   # the KB note (filename matches directory)
│           └── data/               # entry-local artifacts
│               ├── source-notes.md
│               ├── script.sh
│               ├── config.yaml
│               └── exported-log.txt
└── corpus/                         # full source documentation collections
    ├── README.md                   # what a corpus is and how to add one
    ├── _template/corpus.yaml       # manifest template for a new corpus
    └── products/
        └── {product}/              # one corpus collection per product
            ├── corpus.yaml         # required provenance manifest
            └── docs/               # the imported documentation tree
```

- **Directory = KB.** Every entry lives at `kb/{topic}/kbNNNN-short-title/kbNNNN-short-title.md` where `NNNN` is a zero-padded 4-digit number, globally unique across all topics, and `short-title` is a lowercase kebab-case slug derived from the title (3-4 keywords is plenty).
- **Entry-local artifacts go in `data/`.** When a KB includes source material, raw notes, transcripts, pasted docs, scripts, configs, inventories, diagrams, screenshots, exported logs, generated outputs, or other files, place them in a `data/` subdirectory inside the entry directory. No ID prefix is needed on filenames inside `data/` because the parent directory already carries the ID.
- **Global agent skills go in `.agents/skills/`.** Native `.agents/skills/<name>/SKILL.md` files are immediately discoverable workflows for maintaining KB quality. Do not bury global skills inside an entry's `data/` directory.
- **Topics** are lowercase kebab-case folders (`kb/git/`, `kb/cloud/`, `kb/incident-response/`). Reuse an existing folder before creating a new one.

## KB vs Corpus

This repo holds two kinds of knowledge, kept deliberately separate so people and agents never confuse them:

- **`kb/` is curated knowledge.** Authored, summarized entries with stable `kbNNNN` IDs, indexed in `INDEX.md`. This is *what you know*: conventions, how-tos, runbooks, decisions.
- **`corpus/` is source knowledge.** Complete or near-complete upstream documentation preserved verbatim, indexed in `CORPUS_INDEX.md`. This is *what you have*: full product docs, API references, imported Markdown trees.

A corpus is a collection of source material gathered for retrieval and reference. For example, to give an agent the full Helm documentation, import it as a corpus at `corpus/products/helm/` rather than trying to compress it into a single KB entry. Curated KB entries can then reference the corpus for deep detail.

See [corpus/README.md](corpus/README.md) for the corpus workflow and [CORPUS_INDEX.md](CORPUS_INDEX.md) for the discovery index.

## Adding An Entry Manually

1. Pick the next ID: open `INDEX.md`, find the highest `kbNNNN`, add 1, zero-pad to 4 digits.
2. Pick or create a topic folder under `kb/`.
3. Pick a short kebab-case slug from the title, such as `ssh-key-rotation`.
4. Create the directory `kb/{topic}/kbNNNN-{slug}/`.
5. Copy `_template/kb.md` to `kb/{topic}/kbNNNN-{slug}/kbNNNN-{slug}.md` (rename the file to match the directory stem).
6. Fill in the frontmatter:
   - `id` matches the ID prefix, e.g. `kb0042`.
   - `title`: short noun phrase or imperative, <=80 chars.
   - `description`: one sentence, <=120 chars; this is the primary search text.
   - `tags`: 3-7 lowercase kebab-case tokens; check `tags.md` and reuse existing tags before inventing new ones.
   - `aliases`: optional Obsidian-friendly alternative names, or `[]`.
   - `type`: `kb`, `runbook`, or `script`.
   - `scripts`: optional list of script paths relative to the entry directory, e.g. `[data/rotate-key.sh]`.
   - `status`: `active` for new entries.
   - `last_verified`: today's date (`YYYY-MM-DD`).
   - `data_gaps`: list of claims or details you could not verify (empty list `[]` if none).
   - `created` / `updated`: today's date (`YYYY-MM-DD`).
7. Write the body. For runbooks, use Symptoms -> Diagnosis -> Resolution -> Verification -> Rollback. For scripts, use Context -> Usage -> Parameters -> Example Output -> Gotchas.
8. If this KB includes accompanying artifacts:
   - Create `kb/{topic}/kbNNNN-{slug}/data/` and place source material, raw notes, transcripts, pasted docs, scripts, configs, inventories, diagrams, screenshots, exported logs, generated outputs, etc. inside.
   - Scripts must have a shebang (`#!/usr/bin/env bash`, `#!/usr/bin/env python3`, etc.), be `chmod +x`, and include a usage comment near the top.
   - List the script paths in the frontmatter `scripts:` field, e.g. `[data/rotate-key.sh]`.
9. Regenerate the index: `python3 tools/generate_index.py`
10. Validate: `python3 tools/validate.py`

To have an agent do this, say **"turn this into a KB"** and provide the source material. The agent follows [AGENTS.md](AGENTS.md). For a contributor checklist, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Entry Types

Use `type: kb` for reference docs, how-tos, explainers, and conventions.

Use `type: runbook` for operational response steps: symptoms, diagnosis, resolution, verification, and rollback.

Use `type: script` when the main deliverable is one or more executable files. Put scripts in `data/`, list them in frontmatter, include a usage comment, and make them executable.

## Link Inbox

Use [kb/links/kb0003-link-inbox/kb0003-link-inbox.md](kb/links/kb0003-link-inbox/kb0003-link-inbox.md) to save URLs that are useful but do not yet need a dedicated KB entry. The workflow lives at [.agents/skills/kb-add-link/SKILL.md](.agents/skills/kb-add-link/SKILL.md). Keep one canonical entry per normalized URL, preserve repeated sightings with `Seen:` lines, and avoid saving sensitive URLs, credentials, signed links, session IDs, or private customer data.

## Agent Skills

Native [.agents/skills/](.agents/skills/) contains reusable, agent-agnostic workflows for maintaining KB quality, one `SKILL.md` per skill:

- [kb-add-link](.agents/skills/kb-add-link/SKILL.md)
- [kb-create](.agents/skills/kb-create/SKILL.md)
- [kb-create-corpus](.agents/skills/kb-create-corpus/SKILL.md)
- [kb-maintenance](.agents/skills/kb-maintenance/SKILL.md)
- [kb-plan-context](.agents/skills/kb-plan-context/SKILL.md)
- [kb-save-skill](.agents/skills/kb-save-skill/SKILL.md)
- [kb-search](.agents/skills/kb-search/SKILL.md)

## Searching

The fastest path is `rg` from the repo root.

```bash
# Search the index for a term (titles, descriptions, tags, paths)
rg -i "rebase" INDEX.md

# Full-text search across all entries
rg -i "force-with-lease" kb/

# Filter by tag (frontmatter)
rg -n "^tags:.*\\bgit\\b" kb/

# List all KBs in a topic
ls kb/git/

# List entry-local artifacts for a specific KB
ls kb/{topic}/kbNNNN-{slug}/data/

# Survey existing tags so you can reuse them
rg -h "^tags:" kb/ | tr -d '[]' | tr ',' '\n' | sed 's/tags://' | sort -u

# Find KBs that include scripts
rg "^scripts:" kb/

# Find stale entries
rg "^last_verified:" kb/ | sort -t: -k3

# Discover a source-doc collection, then search its full text
rg -i "<term>" CORPUS_INDEX.md
rg -i "<term>" corpus/
```

When linking between entries, use the ID inline (e.g. `kb0001`) and a relative markdown link to the note path when helpful, e.g. `[SSH key rotation](../kb0042-ssh-key-rotation/kb0042-ssh-key-rotation.md)` for same-topic peers.

## Obsidian

This repo opens cleanly as an Obsidian vault.

- The `kbNNNN-short-title.md` stems keep each note unique in the quick switcher, graph view, and backlinks panel.
- Standard Markdown links are preferred because they work in Obsidian, Git hosts, editors, and CLI renderers.
- Use the `aliases:` frontmatter field to add friendlier display names when useful.

## Conventions

- **IDs are permanent.** Do not renumber. If an entry is obsolete, set `status: deprecated` in the frontmatter; do not delete the file.
- **Status lifecycle.** `active` -> `deprecated` -> `archived`. New entries start as `active`. Set `status: deprecated` when the content is no longer recommended. Set `status: archived` when it is purely historical.
- **Verify regularly.** When you re-confirm a KB is still accurate, bump `last_verified` to today.
- **Track unknowns.** If a KB has claims you could not verify or information you know is incomplete, list them in the `data_gaps` frontmatter field.
- **Tag hygiene.** Lowercase kebab-case. Check `tags.md` for the canonical list. Prefer broad tags (`git`) over hyper-specific tags (`git-rebase-force-with-lease`) unless the broad tag is too noisy.
- **One topic per folder.** If a folder grows past roughly 30 entries, consider splitting by sub-topic.
- **One primary note per entry.** The note filename stem must equal the entry directory name (`kbNNNN-short-title`).
- **No secrets.** Redact tokens, credentials, private URLs, customer data, and anything that should not be shared.
- **Commands in fenced blocks.** Always quote exact shell commands so they can be copied.
- **Scripts are self-contained.** Every script must have a shebang, be `chmod +x`, include a usage comment near the top, and never contain secrets.
- **Link related KBs.** Cross-reference by ID in a `## References` section at the bottom.
- **Keep `data/` entry-local.** Source material, raw notes, transcripts, pasted docs, scripts, configs, inventories, diagrams, screenshots, exported logs, generated outputs, and other files that belong with one KB live under that KB's `data/`.
- **Keep `.agents/skills/` global.** Skills are agent-agnostic workflows for maintaining KB quality and live at `.agents/skills/<name>/SKILL.md`, the native, portable skill location.

## Tooling

```bash
python3 tools/generate_index.py    # regenerate INDEX.md from frontmatter
python3 tools/validate.py          # check frontmatter, INDEX consistency, file integrity
```

## Seeing It In Action

[kb/meta/kb0001-kb-framework/kb0001-kb-framework.md](kb/meta/kb0001-kb-framework/kb0001-kb-framework.md) documents the framework itself and serves as a neutral worked example.
