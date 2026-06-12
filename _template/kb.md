---
id: kbNNNN
title: Short title (noun phrase or imperative, <= 80 chars)
description: One sentence, <= 120 chars; front-load key nouns because this is primary search text.
tags: [tag-one, tag-two, tag-three]
aliases: []
type: kb
status: active
last_verified: YYYY-MM-DD
data_gaps: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

<!-- markdownlint-disable MD024 MD025 MD059 MD060 -->

# {Title}

<!--
  Copy this file into a new entry directory and rename it to match the entry stem:

  kb/{topic}/kbNNNN-short-title/kbNNNN-short-title.md

  Put entry-local artifacts in data/: source material, raw notes, transcripts,
  pasted docs, scripts, configs, inventories, diagrams, screenshots, exported
  logs, generated outputs, and other files that belong with this KB.
  Files in data/ inherit context from the parent entry, so use descriptive
  filenames without repeating the KB ID prefix.

  Pick ONE body shape below and delete the others.
  - Use the "kb" shape for references, how-tos, explainers, and conventions.
  - Use the "runbook" shape (type: runbook in frontmatter) for operational responses.
  - Use the "script" shape (type: script in frontmatter) when the primary deliverable
    is executable scripts. Add scripts: [data/script-name.sh] to frontmatter.
  Delete this comment when you are done.
-->

<!-- ===== kb shape ===== -->

## Context

Why this exists / when to use it.

## Steps

1. ...
2. ...
3. ...

## Gotchas

- ...
- ...

## References

- Related KBs: `kbNNNN`
- External: [link title](https://example.com)
- Source material: [data/source-notes.md](data/source-notes.md)

<!-- ===== runbook shape ===== -->

## Symptoms

What the user/operator sees when this fires.

## Diagnosis

How to confirm it is this issue. Include commands, dashboards, or log queries.

```bash
# diagnostic command
```

## Resolution

Step-by-step fix.

```bash
# fix command
```

## Verification

How to confirm the fix worked.

## Rollback

How to undo if the resolution made things worse.

## References

- Related KBs: `kbNNNN`
- Runbook source / postmortem: [link](https://example.com)
- Supporting logs or notes: [data/example-log.txt](data/example-log.txt)

<!-- ===== script shape ===== -->

## Context

What this script does and when to use it.

## Usage

```bash
./data/verb-noun.sh [OPTIONS] <args>
```

## Parameters

| Flag / Arg | Required | Description |
|------------|----------|-------------|
| `<arg1>` | yes | ... |
| `--flag` | no | ... |

## Example Output

```text
$ ./data/verb-noun.sh example-arg
Expected output here...
```

## Gotchas

- ...
- ...

## References

- Related KBs: `kbNNNN`
- External: [link title](https://example.com)
- Supporting files: [data/config.yaml](data/config.yaml)
