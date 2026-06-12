---
id: kb0002
title: Agent skills for KB maintenance
description: Agent-agnostic skills for creating, searching, auditing, and preserving this knowledge base.
tags: [meta, conventions, kb-system, agents, skills]
aliases: [Knowledge base agent skills, KB skills]
type: kb
status: active
last_verified: 2026-06-12
data_gaps: []
created: 2026-06-12
updated: 2026-06-12
---

## Context

This entry catalogs the reusable agent skills that help maintain this knowledge base without tying the framework to a specific agent product or packaging format.

A skill is a reusable agent capability: a plain-language workflow that tells an agent how to perform a recurring job consistently. In this starter KB, skills are immediately discoverable at the repository root:

```text
skills/
```

The skill files are not KB entries. They are root-level operating instructions for agents. This `kb0002` entry explains why they exist, keeps them visible in the generated KB index, and links them to the framework conventions.

## Skills

- [kb-add-link](../../../skills/kb-add-link.md) -- save, normalize, deduplicate, and annotate URLs in the link inbox.
- [kb-create](../../../skills/kb-create.md) -- create, update, and deprecate KB entries while preserving framework invariants.
- [kb-maintenance](../../../skills/kb-maintenance.md) -- audit KB purity, shareability, links, tags, stale entries, and framework drift.
- [kb-plan-context](../../../skills/kb-plan-context.md) -- gather relevant KB context before planning or scoping work.
- [kb-save-skill](../../../skills/kb-save-skill.md) -- preserve a reusable agent skill as a root-level Markdown workflow.
- [kb-search](../../../skills/kb-search.md) -- search and answer from KB content with citations.

## Layout

```text
skills/
├── kb-add-link.md
├── kb-create.md
├── kb-maintenance.md
├── kb-plan-context.md
├── kb-save-skill.md
└── kb-search.md
```

Keep global agent skills at `skills/*.md` so agents can find them quickly. Keep entry-local artifacts under the relevant KB entry's `data/` directory.

## Updating Skills

When adding or changing a skill:

1. Put the skill at `skills/<name>.md` with a lowercase kebab-case filename.
2. Describe the trigger, purpose, workflow, boundaries, and expected output.
3. Keep the skill product-neutral: do not require a specific agent runtime or packaging format.
4. Update this catalog entry.
5. Update [README.md](../../../README.md), [AGENTS.md](../../../AGENTS.md), or [kb0001](../kb0001-kb-framework/kb0001-kb-framework.md) if the new skill changes core KB behavior.
6. Run `python3 tools/generate_index.py` if this entry's frontmatter or path changed, then run `python3 tools/validate.py`.

## Gotchas

- Do not confuse generic agent skills with any tool-specific package file or loader convention.
- Root-level `skills/*.md` files are global repository guidance. Entry-local source material, scripts, logs, transcripts, diagrams, and generated outputs belong under that entry's `data/` directory.
- Skills should never contain secrets, private identifiers, absolute home paths, or environment-specific assumptions.
- The [kb-maintenance](../../../skills/kb-maintenance.md) skill should be run before sharing a copy of the KB.

## References

- [How this KB framework works](../kb0001-kb-framework/kb0001-kb-framework.md)
- [Link inbox](../../links/kb0003-link-inbox/kb0003-link-inbox.md)
