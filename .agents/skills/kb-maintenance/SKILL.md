---
name: kb-maintenance
description: Audit KB purity, shareability, links, tags, stale entries, corpus provenance, and framework drift. Use after manual edits, merges, large imports, skill changes, or before sharing a clean copy of the KB.
---

# KB Maintenance Skill

## Purpose

Audit the knowledge base for structural integrity, shareability, and KB purity.

Use this skill after manual edits, merges, large content imports, skill changes, or before sharing a clean copy of the KB.

## Workflow

1. Regenerate the index if frontmatter, paths, titles, descriptions, tags, status, or entry files changed:

   ```bash
   python3 tools/generate_index.py
   ```

2. Validate structure:

   ```bash
   python3 tools/validate.py
   ```

3. Scan for secrets and private material before sharing (includes `corpus/`, which holds imported source docs):

   ```bash
   rg -i "token|secret|password|credential|private key|api[_-]?key" .
   ```

4. Scan for local-machine and personal identifiers that should not appear in a shareable starter:

   ```bash
   rg -i "/Users/|/home/|C:\\\\Users|user@example|localhost:[0-9]+" .
   ```

5. Scan for tool-specific leakage when the clean KB should stay agent-agnostic. The native skill layout `.agents/skills/<name>/SKILL.md` is intentional framework content, not leakage; focus on product-specific paths and packaging:

   ```bash
   rg -i "cur[s]or|\\.cur[s]or|skills-cur[s]or|\\.claude" .
   ```

6. Check relative links after moves or renames. Prefer full relative paths between KB entries.
7. Check freshness:

   ```bash
   rg "^last_verified:" kb/ | sort -t: -k3
   ```

8. Check tag hygiene. Unknown tags should be added to `tags.md` or replaced with canonical tags.
9. Verify support files:
   - Entry-local source material, raw notes, transcripts, pasted docs, scripts, configs, inventories, diagrams, screenshots, exported logs, generated outputs, and other accompanying artifacts belong under the relevant entry's `data/` directory.
   - Native agent skills live at `.agents/skills/<name>/SKILL.md`; they are global framework content, not entry-local support files.
   - Scripts listed in frontmatter must exist, be executable, have a shebang, and include a usage comment.
10. Verify the corpus:
    - Each collection under `corpus/{category}/{slug}/` has a `corpus.yaml` manifest with provenance fields filled in (source_url, version, retrieved, license, update_method, privacy).
    - Every collection has a row in `CORPUS_INDEX.md`, and every `CORPUS_INDEX.md` row maps to a real collection.
    - `corpus/` contains no `kbNNNN` IDs and no entries leak into `INDEX.md`.
    - Corpus docs are free of secrets, signed URLs, internal hostnames, and customer data.
    - Prefer Markdown/text; flag large binaries or archives that should not be committed.
11. Check framework alignment: `README.md`, `AGENTS.md`, `kb0001`, `kb0002`, `tags.md`, `_template/kb.md`, `corpus/README.md`, `CORPUS_INDEX.md`, and `.agents/skills/*/SKILL.md` should describe the same conventions.

## Completion

Report:

- Validation result.
- Whether `INDEX.md` was regenerated.
- Any shareability or privacy findings.
- Any stale entries, unknown tags, broken links, or framework drift found.
- Files changed, if maintenance included fixes.
