---
name: kb-update-from-reference
description: Update a consumer knowledge base from the reference KB framework repository while preserving consumer-owned content. Use when the user wants to pull framework updates, sync skills/tools, or upgrade their KB from upstream.
---

# KB Update From Reference Skill

## Purpose

Update a downstream (consumer) knowledge base with the latest framework files from the reference KB repository this framework was copied from, without clobbering the consumer's own entries, corpus imports, or local configuration.

Use this skill when the user asks to "update from the reference KB", "pull the latest framework changes", "sync skills and tools from upstream", "upgrade my knowledge base", or otherwise wants to refresh framework mechanics from the source repository.

## Source Of Truth

The reference repository is canonical for **framework mechanics**: agent instructions, skills, tooling, templates, and conventions. Each consumer repository is canonical for **its own knowledge**: `kb/` entries, `corpus/` imports, the generated indexes, and local configuration.

Before updating, read `AGENTS.md` at the consumer repository root. Treat it as canonical if this skill and `AGENTS.md` disagree. The update must never weaken the hard rules in `AGENTS.md` (permanent IDs, no secrets, no deletions of KB entries).

## Terminology

- **Reference repo** -- the upstream framework source this KB was copied or cloned from.
- **Consumer repo** -- the current working knowledge base that wants the update.
- **Framework-owned files** -- mechanics shipped by the framework and expected to track upstream.
- **Consumer-owned files** -- knowledge and configuration the consumer authored and owns.

## File Ownership

Sync framework-owned paths by default:

- `AGENTS.md`, `CLAUDE.md` (if present)
- `README.md`, `CONTRIBUTING.md`
- `_template/` (KB entry scaffold)
- `tools/` (`generate_index.py`, `validate.py`, and peers)
- `.agents/skills/` (all skills, including this one)
- `corpus/README.md`, `corpus/_template/`
- `tags.md` (treat as a merge: keep consumer-added tags, add new reference tags)

Protect consumer-owned paths by default; never overwrite without explicit user instruction:

- `kb/**` (all curated entries, including `kb/meta/*` once the consumer has edited them)
- `corpus/*/*/docs/**` and consumer `corpus.yaml` manifests
- `INDEX.md`, `CORPUS_INDEX.md` (generated locally; regenerate instead of copying)
- `.gitignore` and other local configuration the consumer customized
- Any private data, notes, or `data/` artifacts

Special cases:

- `kb/meta/kb0001-kb-framework` and `kb/meta/kb0002-agent-skills` are framework example entries but are consumer-editable. Treat them as `review-required`: surface upstream changes, but do not overwrite consumer edits silently.
- `tags.md` is a union merge, not an overwrite.

## Identify The Reference Source

Determine where to pull from, in this order:

1. A user-provided path or repository URL.
2. A configured git remote that points at the framework (commonly `upstream`, sometimes `origin`):

   ```bash
   git remote -v
   ```

3. Ask the user for the reference location if neither is available.

Acquire a clean copy of the reference for comparison without disturbing the working tree:

```bash
# remote URL
git clone --depth 1 <reference-url> /tmp/kb-reference

# or a local reference path: use it directly as the comparison source
```

## Conflict Policy

Apply per-file:

- `fast-forward` -- overwrite a framework-owned file only when the consumer copy is unchanged from its previous reference version (or byte-identical to the new one). Safe to apply automatically.
- `review-required` -- a framework-owned file has consumer edits. Leave it untouched, report it, and offer a suggested merge or a diff. Applies to framework example entries (`kb0001`, `kb0002`) and any locally edited framework file.
- `never` -- consumer-owned `kb/` entries, corpus docs, generated indexes, and private/local configuration are never overwritten by an update. Bring in reference KB content only if the user explicitly asks, and then via the normal `kb-create` workflow with new IDs, not by copying.

## Workflow

1. **Confirm intent.** Verify the user wants a framework update, not new KB content. If they want to import reference knowledge entries, use [kb-create](../kb-create/SKILL.md) instead.
2. **Inspect the working tree.** Run `git status`. If framework-owned files have uncommitted local changes, stop and ask before overwriting; recommend committing or stashing first.
3. **Identify and acquire the reference** (see above).
4. **Diff framework-owned paths** between consumer and reference. Classify each changed file using the conflict policy.
5. **Apply `fast-forward` updates** to unchanged framework files.
6. **Report `review-required` files** with diffs; apply only what the user approves.
7. **Do not touch `never` paths.** Leave all consumer `kb/` entries, corpus docs, and local config in place.
8. **Merge `tags.md`** as a union of consumer and reference tags.
9. **Regenerate the index** only if KB frontmatter, paths, titles, descriptions, tags, or status changed:

   ```bash
   python3 tools/generate_index.py
   ```

10. **Validate:**

    ```bash
    python3 tools/validate.py
    ```

11. **Verify framework alignment** (see below).

## Verify

- `python3 tools/validate.py` passes.
- `INDEX.md` was regenerated only if KB frontmatter or paths changed; it still maps one-to-one to `kb/` entries.
- No consumer-owned `kb/` entry, corpus doc, or private file was overwritten.
- `README.md`, `AGENTS.md`, `kb0001`, `kb0002`, `_template/kb.md`, and `.agents/skills/*/SKILL.md` describe the same conventions after the update.

## Boundaries

- Read-only against the reference: never push consumer content upstream as part of an update.
- Never delete a consumer KB entry or directory; framework updates only add or refresh framework-owned files.
- Never overwrite consumer-authored content or generated indexes without explicit approval.
- Never introduce secrets, absolute home paths, or tool-specific assumptions from the reference into the consumer repo; re-run the privacy scan from [kb-maintenance](../kb-maintenance/SKILL.md) if unsure.

## Completion

Report:

- The reference source used and how it was identified.
- Framework files updated (`fast-forward`), files left for review (`review-required`), and files intentionally untouched (`never`).
- Whether `tags.md` was merged and whether `INDEX.md` was regenerated.
- Validation result and any framework drift or conflicts the user still needs to resolve.
