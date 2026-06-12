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

3. Scan for secrets and private material before sharing:

   ```bash
   rg -i "token|secret|password|credential|private key|api[_-]?key" .
   ```

4. Scan for local-machine and personal identifiers that should not appear in a shareable starter:

   ```bash
   rg -i "/Users/|/home/|C:\\\\Users|user@example|localhost:[0-9]+" .
   ```

5. Scan for tool-specific leakage when the clean KB should stay agent-agnostic:

   ```bash
   rg -i "cur[s]or|\\.cur[s]or|S[K]ILL.md|skills-cur[s]or" .
   ```

6. Check relative links after moves or renames. Prefer full relative paths between KB entries.
7. Check freshness:

   ```bash
   rg "^last_verified:" kb/ | sort -t: -k3
   ```

8. Check tag hygiene. Unknown tags should be added to `tags.md` or replaced with canonical tags.
9. Verify support files:
   - Entry-local source material, raw notes, transcripts, pasted docs, scripts, configs, inventories, diagrams, screenshots, exported logs, generated outputs, and other accompanying artifacts belong under the relevant entry's `data/` directory.
   - Root-level `skills/*.md` files are global agent skills, not entry-local support files.
   - Scripts listed in frontmatter must exist, be executable, have a shebang, and include a usage comment.
10. Check framework alignment: `README.md`, `AGENTS.md`, `kb0001`, `kb0002`, `tags.md`, `_template/kb.md`, and `skills/*.md` should describe the same conventions.

## Completion

Report:

- Validation result.
- Whether `INDEX.md` was regenerated.
- Any shareability or privacy findings.
- Any stale entries, unknown tags, broken links, or framework drift found.
- Files changed, if maintenance included fixes.
