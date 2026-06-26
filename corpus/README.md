# Documentation Corpus

The `corpus/` directory holds **complete or near-complete source documentation** preserved for retrieval and reference. A *corpus* is a collection of source material gathered so that humans and agents can search the original text directly.

This is deliberately different from `kb/`:

| | `kb/` | `corpus/` |
| --- | --- | --- |
| Contains | Authored, curated knowledge | Source / upstream documentation |
| Unit | One `kbNNNN` entry per topic | One corpus collection per product |
| Voice | Your interpretation, summaries, runbooks | Verbatim or lightly processed source docs |
| IDs | Stable `kbNNNN` IDs | No `kbNNNN` IDs |
| Index | `INDEX.md` | `CORPUS_INDEX.md` |
| Lifecycle | Hand-maintained, verified | Re-imported / refreshed from source |

In short: **`kb/` is what you know; `corpus/` is what you have.** When a question needs deep product detail, agents pull from the corpus. When a question needs your conventions and decisions, agents use the KB.

## Layout

```text
corpus/
├── README.md
├── _template/
│   └── corpus.yaml         # copy into each new corpus as its manifest
└── products/
    └── helm/
        ├── corpus.yaml     # required manifest (provenance + metadata)
        ├── README.md       # optional human overview of this corpus
        └── docs/           # the actual imported documentation tree
            ├── intro.md
            └── ...
```

- **Group by category, then collection.** Today the main category is `products/`. Add other top-level categories (e.g. `standards/`, `apis/`) only when products is genuinely the wrong fit.
- **One collection per directory.** Each collection (e.g. `products/helm/`) is a single corpus with its own `corpus.yaml`.
- **Keep the source structure.** Mirror the upstream documentation layout under `docs/` so links and navigation stay meaningful.

## Naming

- Category and collection directories are lowercase kebab-case: `corpus/products/helm/`, `corpus/products/argo-cd/`.
- Do not use `kbNNNN` IDs anywhere under `corpus/`. IDs belong to curated KB entries only.
- Keep upstream filenames where practical so cross-references inside the docs keep working.

## Required manifest: `corpus.yaml`

Every collection must include a `corpus.yaml` at its root. Copy [_template/corpus.yaml](_template/corpus.yaml) and fill it in. The manifest captures provenance so the corpus stays trustworthy and refreshable, and it powers `CORPUS_INDEX.md`.

Minimum fields:

- `name` -- human title of the collection (e.g. `Helm`).
- `slug` -- directory slug (e.g. `helm`).
- `description` -- one line; this is primary discovery text.
- `source_url` -- where the docs came from.
- `version` -- upstream version or release the snapshot represents.
- `retrieved` -- `YYYY-MM-DD` the content was imported or last refreshed.
- `license` -- upstream license and any usage constraints.
- `update_method` -- how to refresh (command, script, or manual steps).
- `formats` -- formats present (e.g. `[markdown]`).
- `excludes` -- what was intentionally left out (e.g. binaries, images).
- `privacy` -- confirmation there is no private or sensitive material.
- `aliases` -- alternate search terms (e.g. `[charts, helm charts]`).
- `related_kb` -- optional list of `kbNNNN` IDs that reference this corpus.

## Adding a corpus

For the full agent workflow, including how to find and collect source docs, follow [kb-create-corpus](../.agents/skills/kb-create-corpus/SKILL.md).

1. Pick a category (usually `products/`) and a lowercase kebab-case slug.
2. Create `corpus/{category}/{slug}/`.
3. Copy `corpus/_template/corpus.yaml` into it and fill in every field.
4. Import the documentation under `docs/`, preserving the upstream structure.
5. Prefer Markdown or plain text. Avoid committing large binaries, archives, or images unless explicitly needed (the repo `.gitignore` already excludes most archive types).
6. Remove or redact anything private: secrets, tokens, signed URLs, internal hostnames, customer data.
7. Add a row to [CORPUS_INDEX.md](../CORPUS_INDEX.md) for the new collection.
8. If a KB entry relies on this corpus, link to it from that entry and list the `kbNNNN` ID under `related_kb`.

## How agents should use the corpus

When answering knowledge questions, search in this order:

1. Search `INDEX.md` and `kb/` for curated guidance.
2. Search `CORPUS_INDEX.md` and `corpus/` for full source documentation.
3. If a KB entry references a corpus, follow that reference for deeper product detail.
4. If no KB entry matches but corpus material does, answer from the corpus and make clear it is **source documentation, not curated KB guidance**.
5. If KB guidance and corpus docs conflict, prefer the KB for local conventions and cite the corpus for upstream behavior.

## What does not belong here

- Curated notes, runbooks, and how-tos -- those are `kb/` entries.
- Artifacts that support a single KB entry -- those go in that entry's `data/` directory.
- Global agent workflows -- those are native `.agents/skills/<name>/SKILL.md` files.
- Secrets, credentials, private URLs, or customer data -- never commit these.
