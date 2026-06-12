# KB Save Skill

## Purpose

Preserve a reusable agent skill as a root-level Markdown workflow in this repository.

Use this skill when the user asks to archive, preserve, make portable, or update a KB-related agent skill.

## Terminology

In this repository, a skill is an agent-agnostic reusable capability documented in plain Markdown. It is not tied to any specific runtime, loader, or package format.

## Workflow

1. Parse the requested skill name, e.g. `kb-maintenance`.
2. Confirm the skill is KB-related and belongs in this shareable starter. If it is product-specific, private, or not about maintaining the KB, ask before adding it.
3. Review the source material for secrets, credentials, private identifiers, absolute home paths, and tool-specific assumptions.
4. Create or update `skills/<skill-name>.md` with:
   - Purpose.
   - When to use it.
   - Source of truth, if any.
   - Workflow.
   - Boundaries.
   - Completion or output contract.
5. Update `kb/meta/kb0002-agent-skills/kb0002-agent-skills.md` so the catalog lists the skill and explains its role.
6. Update `README.md`, `AGENTS.md`, or `kb0001` if the skill changes core KB behavior.
7. Run validation from the repository root:

   ```bash
   python3 tools/validate.py
   ```

   Regenerate `INDEX.md` only if KB frontmatter, status, title, description, tags, or path changed.

## Conversion Notes

If a skill comes from a tool-specific format, convert it to plain Markdown before saving it here:

- Remove runtime-specific frontmatter.
- Remove tool-specific invocation mechanics.
- Replace absolute machine paths with repository-relative paths.
- Keep the reusable workflow and decision rules.

## Edge Cases

- If no skill name is provided, ask for one.
- If the archive already contains that skill, update the existing file unless the user asked for a diff first.
- If the source contains private or product-specific material, stop and ask whether to redact, skip, or keep it outside the clean KB.
