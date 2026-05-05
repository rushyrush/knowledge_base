# Personal KB Framework

A shareable starter framework for building a personal knowledge base with plain Markdown, stable IDs, searchable metadata, optional support files, and AI-agent-friendly conventions.

It works as a normal folder of Markdown files, an Obsidian vault, and a command-line searchable reference library.

It is designed for humans and AI agents to share and expand together: humans contribute context and judgment, while agents help turn raw source material into durable KB entries.

## Quickstart

1. Copy or clone this repository for your own KB.
2. Open it in your editor or in Obsidian as a vault.
3. Read the example entry at [kb/meta/kb0001-kb-framework/kb0001-kb-framework.md](kb/meta/kb0001-kb-framework/kb0001-kb-framework.md).
4. Create your first entry from [_template/kb.md](_template/kb.md), or give your AI agent source material and ask it to **"turn this into a KB"**. Good source material includes files, shell-session notes, chat transcripts, or text pasted directly into agent chat.
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
├── README.md                # how to use the framework
├── CONTRIBUTING.md          # lightweight contribution checklist
├── AGENTS.md                # instructions agents follow when adding entries
├── INDEX.md                 # searchable index generated from frontmatter
├── _template/kb.md          # copy this when adding a new entry
├── tags.md                  # starter tag taxonomy
├── tools/                   # index generator and validator
└── kb/
    └── {topic}/             # one folder per topic, lowercase kebab-case
        └── kbNNNN-short-title/
            ├── kbNNNN-short-title.md
            └── data/        # optional support files for this entry
```

Each entry directory contains one primary Markdown note. The note filename is unique and readable for Obsidian, while the entry directory keeps related support files nearby.

## Entry Convention

- **ID:** every entry gets a permanent `kbNNNN` ID, such as `kb0042`.
- **Directory:** use `kb/{topic}/kbNNNN-short-title/`.
- **Note:** use `kb/{topic}/kbNNNN-short-title/kbNNNN-short-title.md`.
- **Support files:** put scripts, configs, screenshots, exports, and other files in `data/` inside the entry directory.
- **Topics:** use lowercase kebab-case folders such as `git`, `aws-ec2`, or `incident-response`.

## Adding An Entry Manually

1. Pick the next ID by opening `INDEX.md`, finding the highest `kbNNNN`, adding 1, and zero-padding to four digits.
2. Pick or create a topic folder under `kb/`.
3. Create a readable slug from the title, such as `ssh-key-rotation`.
4. Create the entry directory: `kb/{topic}/kbNNNN-ssh-key-rotation/`.
5. Copy `_template/kb.md` to `kb/{topic}/kbNNNN-ssh-key-rotation/kbNNNN-ssh-key-rotation.md`.
6. Fill in the frontmatter:
   - `id` matches the ID prefix, e.g. `kb0042`.
   - `title` is a short noun phrase or imperative, <=80 chars.
   - `description` is one sentence, <=120 chars.
   - `tags` contains 3-7 lowercase kebab-case tokens from `tags.md` where possible.
   - `type` is `kb`, `runbook`, or `script`.
   - `scripts` is optional and lists script paths relative to the entry directory, e.g. `[data/create-user.sh]`.
   - `status` is usually `active` for new entries.
   - `last_verified`, `created`, and `updated` use `YYYY-MM-DD`.
   - `data_gaps` lists unknowns, or `[]` if there are none.
7. Delete unused template sections and write the body.
8. Regenerate the index with `python3 tools/generate_index.py`.
9. Validate with `python3 tools/validate.py`.

To have an agent do this, say **"turn this into a KB"** and provide the source material, such as files, shell-session notes, chat transcripts, or pasted text. The agent follows [AGENTS.md](AGENTS.md).

## Entry Types

Use `type: kb` for reference docs, how-tos, explainers, and conventions.

Use `type: runbook` for operational response steps: symptoms, diagnosis, resolution, verification, and rollback.

Use `type: script` when the main deliverable is one or more executable files. Put scripts in `data/`, list them in frontmatter, include a usage comment, and make them executable.

## Searching

The fastest path is `rg` from the repo root.

```bash
# Search the index for a term in titles, descriptions, tags, and paths
rg -i "rebase" INDEX.md

# Full-text search across entries
rg -i "force-with-lease" kb/

# Filter by tag in frontmatter
rg -n "^tags:.*\\bgit\\b" kb/

# List topics
ls kb/

# List entries in a topic
ls kb/git/

# Find entries that include scripts
rg "^scripts:" kb/

# Find stale entries
rg "^last_verified:" kb/ | sort -t: -k3
```

When linking between entries, use the ID inline, e.g. `kb0001`, and a relative Markdown link when helpful.

## Obsidian Notes

This repository can be opened directly as an Obsidian vault. The hybrid layout keeps each note filename unique for quick switcher, backlinks, graph view, and search results.

Standard Markdown links are preferred because they work in Obsidian, GitHub, Cursor, and command-line rendered Markdown. You can add `aliases:` in frontmatter when you want a friendlier Obsidian display name.

## Conventions

- **IDs are permanent.** Do not renumber or reuse them.
- **One primary note per entry.** The entry directory and note filename should share the same `kbNNNN-short-title` stem.
- **Support files stay local.** Keep related files under the entry's `data/` directory.
- **No secrets.** Do not store tokens, credentials, private URLs, customer data, or anything that should not be shared.
- **Tag hygiene matters.** Reuse `tags.md` first, and prefer broad tags over very narrow one-off tags.
- **Descriptions are search text.** Front-load important nouns so index search works well.
- **Commands go in fenced code blocks.** Use the right language tag when practical.
- **Cross-reference related entries.** Add related IDs in a `## References` section.

## Tooling

```bash
python3 tools/generate_index.py    # regenerate INDEX.md from frontmatter
python3 tools/validate.py          # check frontmatter, paths, index, tags, and scripts
```

## Example

[kb/meta/kb0001-kb-framework/kb0001-kb-framework.md](kb/meta/kb0001-kb-framework/kb0001-kb-framework.md) documents the framework itself and serves as a neutral worked example.
