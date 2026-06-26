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
updated: 2026-06-26
---

## Context

This entry catalogs the reusable agent skills that help maintain this knowledge base without tying the framework to a specific agent product or packaging format.

A skill is a reusable agent capability: a plain-language workflow that tells an agent how to perform a recurring job consistently. In this starter KB, skills use the native, portable layout with one `SKILL.md` per skill:

```text
.agents/skills/<name>/SKILL.md
```

The skill files are not KB entries. They are native operating instructions for agents. This `kb0002` entry explains why they exist, keeps them visible in the generated KB index, and links them to the framework conventions.

## Skills

- [kb-add-link](../../../.agents/skills/kb-add-link/SKILL.md) -- save, normalize, deduplicate, and annotate URLs in the link inbox.
- [kb-create](../../../.agents/skills/kb-create/SKILL.md) -- create, update, and deprecate KB entries while preserving framework invariants.
- [kb-create-corpus](../../../.agents/skills/kb-create-corpus/SKILL.md) -- build a `corpus/` collection of full source documentation from user-provided or agent-collected sources.
- [kb-maintenance](../../../.agents/skills/kb-maintenance/SKILL.md) -- audit KB purity, shareability, links, tags, stale entries, and framework drift.
- [kb-plan-context](../../../.agents/skills/kb-plan-context/SKILL.md) -- gather relevant KB context before planning or scoping work.
- [kb-save-skill](../../../.agents/skills/kb-save-skill/SKILL.md) -- preserve a reusable agent skill as a native `SKILL.md` workflow.
- [kb-search](../../../.agents/skills/kb-search/SKILL.md) -- search and answer from KB content with citations.
- [kb-update-from-reference](../../../.agents/skills/kb-update-from-reference/SKILL.md) -- update a consumer KB from the reference framework repo while preserving consumer-owned content.

## Layout

```text
.agents/skills/
├── kb-add-link/SKILL.md
├── kb-create/SKILL.md
├── kb-create-corpus/SKILL.md
├── kb-maintenance/SKILL.md
├── kb-plan-context/SKILL.md
├── kb-save-skill/SKILL.md
├── kb-search/SKILL.md
└── kb-update-from-reference/SKILL.md
```

Keep global agent skills at `.agents/skills/<name>/SKILL.md` so agents can find them quickly. Keep entry-local artifacts under the relevant KB entry's `data/` directory.

## Updating Skills

When adding or changing a skill:

1. Put the skill at `.agents/skills/<name>/SKILL.md` with a lowercase kebab-case directory name, and give it `name` and `description` frontmatter.
2. Describe the trigger, purpose, workflow, boundaries, and expected output.
3. Keep the skill product-neutral: the `.agents/skills/` layout is portable, so do not require a specific agent runtime beyond the shared `SKILL.md` convention.
4. Update this catalog entry.
5. Update [README.md](../../../README.md), [AGENTS.md](../../../AGENTS.md), or [kb0001](../kb0001-kb-framework/kb0001-kb-framework.md) if the new skill changes core KB behavior.
6. Run `python3 tools/generate_index.py` if this entry's frontmatter or path changed, then run `python3 tools/validate.py`.

## Gotchas

- Do not confuse these agent-neutral skills with any single tool's proprietary package file or loader convention; `.agents/skills/<name>/SKILL.md` is the shared, portable form.
- Native `.agents/skills/<name>/SKILL.md` files are global repository guidance. Entry-local source material, scripts, logs, transcripts, diagrams, and generated outputs belong under that entry's `data/` directory.
- Skills should never contain secrets, private identifiers, absolute home paths, or environment-specific assumptions.
- The [kb-maintenance](../../../.agents/skills/kb-maintenance/SKILL.md) skill should be run before sharing a copy of the KB.

## References

- [How this KB framework works](../kb0001-kb-framework/kb0001-kb-framework.md)
- [Link inbox](../../links/kb0003-link-inbox/kb0003-link-inbox.md)
