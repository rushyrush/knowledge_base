---
id: kb0003
title: Link inbox
description: Starter inbox for saving, deduplicating, and annotating useful URLs before they become KB entries.
tags: [links, research, kb-system, maintenance]
aliases: [Saved links, URL inbox]
type: kb
status: active
last_verified: 2026-06-12
data_gaps: []
created: 2026-06-12
updated: 2026-06-26
---

## Context

Use this entry to save useful URLs that are worth keeping but do not yet need their own KB entry. It is intentionally lightweight: one canonical entry per normalized URL, with notes and repeated sightings preserved in place.

The [kb-add-link](../../../.agents/skills/kb-add-link/SKILL.md) skill can maintain this inbox automatically. The full skill catalog is [Agent skills for KB maintenance](../../meta/kb0002-agent-skills/kb0002-agent-skills.md).

## How To Add Links

Add new links under `## Links`, newest first.

Use this shape:

```markdown
### YYYY-MM-DD - Title

- URL: https://example.com/path
- Tags: topic, docs
- Note: Why this is worth keeping.
- Related KBs: kb0001
- Seen: YYYY-MM-DD - initial save
```

Use `Related KBs: []` when there is no related entry.

## Deduplication

Keep one canonical entry per normalized URL. When the same URL is saved again, add another `Seen:` line or append a short note instead of creating a duplicate heading.

Normalize conservatively:

- Strip tracking-only parameters such as `utm_*`, `fbclid`, `gclid`, `mc_cid`, and `mc_eid`.
- Preserve meaningful query parameters and fragments unless they are clearly only for tracking.
- Keep the original URL if normalization would change what the page shows.

## Gotchas

- Do not save credentials, signed URLs, session IDs, API keys, private keys, or other secret-bearing links.
- Do not save customer data, sensitive internal host details, or private documents unless this KB is allowed to contain them.
- If a link grows into durable instructions, promote it into a normal KB entry and reference that entry here.

## Links

<!-- Add saved links here, newest first. -->

## References

- [How this KB framework works](../../meta/kb0001-kb-framework/kb0001-kb-framework.md)
- [Agent skills for KB maintenance](../../meta/kb0002-agent-skills/kb0002-agent-skills.md)
- [kb-add-link skill](../../../.agents/skills/kb-add-link/SKILL.md)
