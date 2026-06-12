# KB Add Link Skill

## Purpose

Add, track, normalize, and deduplicate links in the KB link inbox.

Use this skill when the user asks to save a URL, track a link, add a link to the KB, or update the link inbox.

## Source Of Truth

Before creating or updating KB content, read `AGENTS.md` at the repository root. Follow that file for KB conventions, verification, ID permanence, tags, and secret handling.

## Link Inbox

The starter link-tracking entry is:

```text
kb/links/kb0003-link-inbox/kb0003-link-inbox.md
```

Find it by `id: kb0003` or title `Link inbox` if the path has moved.

## Workflow

1. Parse one or more URLs and any user-provided title, tags, note, or related KB IDs.
2. Read the link inbox. If it is missing, create it using the standard KB create workflow in `AGENTS.md`, regenerate `INDEX.md`, and run validation.
3. Normalize the URL conservatively:
   - Remove common tracking parameters such as `utm_*`, `fbclid`, `gclid`, `mc_cid`, and `mc_eid`.
   - Preserve meaningful query parameters and fragments unless they are clearly tracking-only.
4. Check for sensitive-looking content before writing:
   - Embedded credentials, tokens, API keys, signatures, signed URLs, session IDs, or private keys.
   - Customer data or sensitive internal host details.
   - If unsure, ask whether to redact, strip, or skip the URL.
5. For public URLs, try to infer a readable title and one-sentence note. Do not force authenticated, private, or blocked pages; use the user's note or a placeholder title instead.
6. Search the inbox for the normalized URL.
7. If the URL already exists, update that entry with a new `Seen:` line or a short additional note instead of creating a duplicate.
8. If the URL is new, append a dated entry under `## Links`, newest first.
9. Run `python3 tools/validate.py` from the repository root. Regenerate `INDEX.md` only if frontmatter, status, title, description, tags, or path changed.

## Entry Format

```markdown
### YYYY-MM-DD - Title

- URL: https://example.com/path
- Tags: topic, docs
- Note: Why this is worth keeping.
- Related KBs: kb0001
- Seen: YYYY-MM-DD - initial save
```

Use `Related KBs: []` when there is no related entry.

## Completion

Report the saved or updated URL title, whether it was new or merged into an existing entry, the inbox path, and validation result.
