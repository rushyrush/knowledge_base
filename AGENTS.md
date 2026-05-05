# AGENTS.md

Instructions for AI agents working in this personal KB framework.

## When the user says "turn this into a KB"

The user will give you a document, a paste of text, or a link. Convert it into a well-formed entry in this KB. Follow the checklist below and do not skip verification.

### Checklist

1. **Determine the type.**
   - `kb` -- reference, how-to, explainer, conventions.
   - `runbook` -- operational response: something is broken, here is what to do.
   - `script` -- primary deliverable is one or more executable scripts; the Markdown entry documents usage.
   - If ambiguous, ask the user.

2. **Pick a topic folder.**
   - List `kb/` and reuse an existing folder if one fits, e.g. `git`, `aws-ec2`, `incident-response`.
   - Only create a new topic if no existing topic fits. Use lowercase kebab-case.
   - If multiple topics could fit, ask the user.

3. **Allocate the next ID.**
   - Read `INDEX.md`, find the largest `kbNNNN`, add 1, and zero-pad to 4 digits.
   - Double-check the ID is unused with `rg "^id: kbNNNN$" kb/`.

4. **Choose a slug.**
   - Create a short lowercase kebab-case slug from the title.
   - Use the hybrid stem `kbNNNN-short-title` for both the entry directory and note filename.

5. **Create the entry directory.**
   - Create `kb/{topic}/kbNNNN-short-title/`.
   - Copy `_template/kb.md` to `kb/{topic}/kbNNNN-short-title/kbNNNN-short-title.md`.
   - If the KB includes scripts, configs, attachments, or other support files, create `data/` inside the entry directory.
   - All scripts must have a shebang and be executable.

6. **Fill the frontmatter.**
   - `id`: matches the ID prefix, e.g. `kb0042`.
   - `title`: noun phrase or imperative, <=80 chars. No trailing period.
   - `description`: one sentence, <=120 chars. Front-load key nouns because this is primary search text.
   - `tags`: 3-7 lowercase kebab-case tokens. Check `tags.md` and reuse existing tags first.
   - `aliases`: optional Obsidian-friendly names.
   - `type`: `kb`, `runbook`, or `script`.
   - `scripts`: optional array of script paths relative to the entry directory, e.g. `[data/create-user.sh]`.
   - `status`: `active` for new entries, `draft` if incomplete.
   - `last_verified`: today's date in `YYYY-MM-DD`.
   - `data_gaps`: list of claims or details you could not verify. Use `[]` if none.
   - `created` and `updated`: today's date in `YYYY-MM-DD`.

7. **Write the body.**
   - Do not dump raw paste. Extract structure: steps, commands, gotchas, references.
   - For `type: kb`, use: Context, Steps or Details, Gotchas, References.
   - For `type: runbook`, use: Symptoms, Diagnosis, Resolution, Verification, Rollback.
   - For `type: script`, use: Context, Usage, Parameters, Example Output, Gotchas, References.
   - Quote exact commands in fenced code blocks with the right language tag.
   - Cross-reference related KBs by ID in the References section.
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
- Type is unclear.
- The source contains apparent secrets, credentials, private URLs, customer data, or other details that should probably be redacted before being written to disk.

Otherwise, do the work and report what you created.

## Other agent tasks

### Updating an existing KB

- Bump the `updated:` field in the frontmatter to today.
- If the content was re-verified as accurate, also bump `last_verified:`.
- If the title, description, tags, status, or path changed, regenerate the index.
- Never change the ID. If the topic or slug is wrong, you may move the entry directory while keeping the same `kbNNNN` ID.

### Deprecating a KB

- Set `status: deprecated` in the frontmatter.
- Add a note at the top of the body explaining why and pointing to any replacement.
- Regenerate the index.

### Searching the KB

Before answering questions from this KB, search both the index and the full text:

```bash
rg -i "{term}" INDEX.md
rg -i "{term}" kb/
```

Cite hits by ID and link to the file with a relative Markdown link.

### Hard rules

- Never reuse or renumber IDs. IDs are permanent.
- Never put secrets in the KB. When in doubt, redact and ask.
- Scripts must have a shebang, be executable, include a short usage comment, and never contain secrets or hardcoded credentials.
- Prefer `tags.md` tags. Check the starter taxonomy before inventing new tags.
- Keep one primary Markdown note per entry directory.
