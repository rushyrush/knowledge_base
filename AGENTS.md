<!-- FOR AI AGENTS - Human readability is a side effect, not the goal -->
<!-- Managed by agent: keep sections and order; edit content, not structure -->
<!-- Last updated: 2026-06-12 | Last verified: 2026-06-12 -->

# AGENTS.md

**Precedence:** the closest `AGENTS.md` to the files you are changing wins. This repository currently has only this root file.

Instructions for agents working in this knowledge base framework.

The KB is organized as a reusable framework: every entry lives at `kb/{topic}/kbNNNN-short-title/kbNNNN-short-title.md`, with optional `data/` beside the note for source material, raw notes, transcripts, pasted docs, scripts, configs, inventories, diagrams, screenshots, exported logs, generated outputs, and other accompanying artifacts. The hybrid stem (matching directory name and note filename) keeps each note unique in Obsidian's quick switcher, backlinks, and graph view while keeping support files local to the entry.

## Project facts

| Area | Fact |
| --- | --- |
| Project type | Markdown knowledge base / Obsidian vault |
| Primary content | KB notes under `kb/{topic}/kbNNNN-short-title/` |
| Automation | Python maintenance scripts in `tools/` |
| Template | `_template/kb.md` |
| Tag source | `tags.md` |
| Index | `INDEX.md`, generated from entry frontmatter |
| Agent skills | Root-level generic skills in `skills/*.md` |
| Scoped agent files | None currently; this root file applies repo-wide |

## Commands

Run commands from the repository root.

| Task | Command |
| --- | --- |
| Regenerate index | `python3 tools/generate_index.py` |
| Validate KB structure | `python3 tools/validate.py` |
| Search index | `rg -i "<term>" INDEX.md` |
| Search entries | `rg -i "<term>" kb/` |
| Filter by tag | `rg -n "^tags:.*\b<tag>\b" kb/` |
| Find script entries | `rg "^scripts:" kb/` |
| Survey existing tags | `rg -h "^tags:" kb/ \| tr -d '[]' \| tr ',' '\n' \| sed 's/tags://' \| sort -u` |

## File map

| Path | Purpose |
| --- | --- |
| `README.md` | Human overview, layout, and manual entry workflow |
| `CONTRIBUTING.md` | Contributor checklist for adding and validating entries |
| `AGENTS.md` | Canonical cross-agent workflow and hard rules |
| `CLAUDE.md` | Symlink compatibility alias to `AGENTS.md` |
| `INDEX.md` | Generated searchable table of all KB entries |
| `tags.md` | Canonical tag vocabulary |
| `_template/kb.md` | Frontmatter and body template for new entries |
| `tools/generate_index.py` | Rebuilds `INDEX.md` from frontmatter |
| `tools/validate.py` | Validates entry layout, frontmatter, scripts, tags, and index consistency |
| `skills/` | Root-level reusable agent skills for maintaining KB quality |
| `kb/` | Topic folders and KB entry directories |

## When the user says "turn this into a KB"

The user will give you a document, a paste of text, or a link. Convert it into a well-formed entry in this KB. Follow the checklist below and do not skip verification.

### Checklist

1. **Determine the type.**
   - `kb` -- reference, how-to, explainer, conventions.
   - `runbook` -- operational response: something is broken, here is what to do.
   - `script` -- primary deliverable is one or more executable scripts; the Markdown entry documents usage.
   - If ambiguous, ask the user.

2. **Pick a topic folder.**
   - List `kb/` and reuse an existing folder if one fits, e.g. `git`, `cloud`, `incident-response`.
   - Only create a new topic if no existing topic fits. Use lowercase kebab-case.
   - If multiple topics could fit, ask the user.

3. **Allocate the next ID.**
   - Read `INDEX.md`, find the largest `kbNNNN`, add 1, and zero-pad to 4 digits.
   - Double-check the ID is unused: `rg "^id: kbNNNN$" kb/` should return nothing.

4. **Choose a slug.**
   - Create a short lowercase kebab-case slug from the title (3-4 keywords is usually enough).
   - Use the hybrid stem `kbNNNN-short-title` for both the entry directory and note filename.

5. **Create the entry directory.**
   - Create `kb/{topic}/kbNNNN-short-title/`.
   - Copy `_template/kb.md` to `kb/{topic}/kbNNNN-short-title/kbNNNN-short-title.md`.
   - If the KB includes source material, raw notes, transcripts, pasted docs, scripts, configs, inventories, diagrams, screenshots, exported logs, generated outputs, or other accompanying artifacts, create `data/` inside the entry directory. Use descriptive filenames without the ID prefix (e.g. `rotate-key.sh`, not `kb0042-rotate-key.sh`) because the parent entry already provides the KB context.
   - All scripts must have a shebang and be executable (`chmod +x`).

6. **Fill the frontmatter.**
   - `id`: matches the ID prefix, e.g. `kb0042`.
   - `title`: noun phrase or imperative, <=80 chars. No trailing period.
   - `description`: one sentence, <=120 chars. Front-load key nouns because this is primary search text.
   - `tags`: 3-7 lowercase kebab-case tokens. **Check `tags.md` and reuse existing tags first.** Survey with:

     ```bash
     rg -h "^tags:" kb/ | tr -d '[]' | tr ',' '\n' | sed 's/tags://' | sort -u
     ```

   - `aliases`: optional Obsidian-friendly alternative names, e.g. `[SSH key rotation]`. Leave as `[]` if none.
   - `type`: `kb`, `runbook`, or `script`.
   - `scripts`: optional array of script paths relative to the entry directory, e.g. `[data/rotate-key.sh]`.
   - `status`: `active` for new entries, `draft` if incomplete.
   - `last_verified`: today's date in `YYYY-MM-DD`.
   - `data_gaps`: list of claims or details you could not verify. Use `[]` if none.
   - `created` and `updated`: today's date in `YYYY-MM-DD`.

7. **Write the body.**
   - **Do not dump raw paste.** Extract structure: steps, commands, gotchas, references.
   - For `type: kb`, use: Context, Steps (or Details), Gotchas, References.
   - For `type: runbook`, use: Symptoms, Diagnosis, Resolution, Verification, Rollback.
   - For `type: script`, use: Context, Usage, Parameters, Example Output, Gotchas, References. The script itself should have a usage comment block at the top.
   - Quote exact commands in fenced code blocks with the right language tag.
   - Cross-reference related KBs by ID in the References section. Use full relative paths to the new note location, e.g. `[SSH key rotation](../kb0042-ssh-key-rotation/kb0042-ssh-key-rotation.md)` for same-topic peers and `../../topic/kbNNNN-slug/kbNNNN-slug.md` across topics.
   - Keep it concise. If the source is long, summarize and link to the source.

8. **Regenerate `INDEX.md`.**
   - Run `python3 tools/generate_index.py` to rebuild the index from frontmatter.
   - Confirm the ID appears once in the table.

9. **Verify before finishing.**
   - The entry exists at `kb/{topic}/kbNNNN-short-title/kbNNNN-short-title.md`.
   - The ID in the directory stem, note filename, frontmatter `id:`, and `INDEX.md` row all match.
   - `rg "^id: kbNNNN$" kb/` returns exactly one hit.
   - `rg "kbNNNN" INDEX.md` returns at least one hit.
   - If scripts are listed in `scripts:`, each file exists under the entry directory and is executable.
   - Run `python3 tools/validate.py`.

### When to ask the user

Ask only when one of these is true:

- Topic folder is genuinely ambiguous between two existing options, or no existing topic fits and you are unsure what to name a new one.
- Type (`kb` vs `runbook` vs `script`) is unclear.
- The source contains apparent secrets, credentials, private URLs, customer data, or other details that should probably be redacted before being written to disk.

Otherwise, do the work and report what you created.

## Other agent tasks

### Updating an existing KB

- Bump the `updated:` field in the frontmatter to today.
- If the content was re-verified as accurate, also bump `last_verified:`.
- If the title, description, tags, status, or path changed, regenerate the index: `python3 tools/generate_index.py`.
- Never change the `id`. If the topic or slug is wrong, you may move the entry directory while keeping the same `kbNNNN` ID; remember to rename the note file to match the new directory stem.

### Deprecating a KB

- Never delete a KB file or directory.
- Set `status: deprecated` in the frontmatter.
- Add a note at the top of the body explaining why and pointing to any replacement.
- Regenerate the index.

### Searching the KB

Before answering questions from this KB, search both the index and the full text:

```bash
rg -i "{term}" INDEX.md
rg -i "{term}" kb/
```

Cite hits by ID (e.g. `kb0042`) and link to the file with a relative markdown link.

### Adding links

Use the link inbox at `kb/links/kb0003-link-inbox/kb0003-link-inbox.md` when the user asks to save, track, or deduplicate a URL. Follow `skills/kb-add-link.md` for the full workflow. Normalize URLs conservatively, strip tracking parameters only when they are clearly tracking-only, and never save credentials, signed URLs, session IDs, private keys, customer data, or other sensitive details without explicit confirmation.

### Maintaining KB purity

Use `skills/kb-maintenance.md` after manual edits, merges, large imports, skill changes, or before sharing a copy of the KB. It checks index validity, structure, stale entries, tags, relative links, private material, tool-specific leakage, and alignment across `README.md`, `AGENTS.md`, `kb0001`, `kb0002`, `_template/kb.md`, and `skills/*.md`.

### Hard rules

- **Never delete a KB file or directory.** If obsolete, set `status: deprecated`.
- **Never reuse or renumber IDs.** IDs are permanent.
- **Never put secrets in the KB.** When in doubt, redact and ask.
- **Scripts must have a shebang** (`#!/usr/bin/env bash`, `#!/usr/bin/env python3`, etc.), be executable (`chmod +x`), include a short usage comment, and never contain secrets or hardcoded credentials.
- **Prefer `tags.md` tags.** Check the canonical tag list before inventing new tags.
- **One primary Markdown note per entry directory.** The note filename stem must equal the entry directory name.
- **Use `data/` for entry-local artifacts.** Source material, raw notes, transcripts, pasted docs, scripts, configs, inventories, diagrams, screenshots, exported logs, generated outputs, and other files that belong with a single KB entry live under that entry's `data/` directory.
- **Use `skills/` for global agent skills.** Root-level `skills/*.md` files are not entry-local artifacts; they are discoverable instructions for maintaining KB quality.

## Scoped agent guidance

No scoped `AGENTS.md` files currently exist. If a subtree needs narrower guidance later, add an `AGENTS.md` in that subtree and keep this section current.
