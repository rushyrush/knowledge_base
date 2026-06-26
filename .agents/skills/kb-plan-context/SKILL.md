---
name: kb-plan-context
description: Gather relevant KB context before planning or scoping work. Use when planning, designing, or scoping work that may intersect known KB entries, runbooks, scripts, conventions, or prior source material.
---

# KB Plan Context Skill

## Purpose

Search this knowledge base and pull concise context relevant to a planning task.

Use this skill when planning, designing, or scoping work that may intersect known KB entries, runbooks, scripts, conventions, or prior source material.

## Workflow

1. Identify trigger terms from the user's request or current plan: nouns, technologies, systems, topics, and likely tags.
2. Search both metadata and full text:

   ```bash
   rg -i "{term}" INDEX.md
   rg -i "{term}" kb/
   ```

3. Read selectively. Open only the most relevant primary notes and, when useful, their `data/` support files.
4. Return a context pack. Do not dump raw search output.
5. Feed the context into the plan with KB IDs cited in-line.

## Output Contract

```markdown
## KB Context
- [kbNNNN](relative/path.md): why this is relevant to the plan

## Planning Constraints
- Constraint or convention from the KB

## Reusable Commands Or Procedures
- Relevant command or procedure if applicable

## Gaps Or Freshness Notes
- Missing, stale, or conflicting KB information
```

Keep the context pack focused. If no relevant entries exist, say so and note any near-misses.

## Boundaries

- Read-only: do not edit KB entries, plan files, or source files.
- Do not invoke broader search workflows unless the user asks.
- Limit KB reads to the most relevant 3-5 entries.
- If the trigger terms are ambiguous, prioritize entries with `type: runbook` or `type: script` over general reference notes.
