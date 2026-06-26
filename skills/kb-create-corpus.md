# KB Create Corpus Skill

## Purpose

Build a corpus collection under `corpus/{category}/{slug}/` from varying sources, whether the user provides the material directly or the agent assembles it from source data found online.

Use this skill when the user asks to "build a corpus", "create a corpus", "import all the docs for X", "give the agent the full docs for X", or otherwise wants complete source documentation preserved for retrieval rather than a curated summary.

If the user instead wants a distilled, summarized entry, use [kb-create](kb-create.md) and the KB workflow instead.

## Source Of Truth

Before creating a corpus, read [corpus/README.md](../corpus/README.md) and the "add this as a corpus" section of `AGENTS.md` at the repository root. Treat them as canonical if this skill and those documents disagree.

## Terminology

- A *corpus* is a collection of source material gathered for retrieval and reference: complete or near-complete upstream documentation kept verbatim.
- `corpus/` is source knowledge; `kb/` is curated knowledge.
- A corpus never gets a `kbNNNN` ID and never appears in `INDEX.md`. Collections are discovered through `CORPUS_INDEX.md`.

## Acquisition Method Ladder

Pick the highest method on this ladder that fits the source. Prefer Markdown or plain text output in every case.

1. **User-provided.** The user hands over a folder, archive, path, or paste. Copy it into `docs/`, preserving the original structure. Record the source as user-provided with the date.
2. **`llms.txt` / `llms-full.txt`.** Many documentation sites publish an LLM-ready full-text file at the site root (for example `https://example.com/llms-full.txt`, falling back to `https://example.com/llms.txt`). If present, fetch it directly; this is the cleanest single-file capture. Record the exact URL.
3. **Upstream docs repo.** Find the canonical source repository (often GitHub or GitLab), shallow-clone it, and copy the documentation subtree (commonly `docs/`) of Markdown files. This gives the best provenance and the easiest refresh:

   ```bash
   git clone --depth 1 https://github.com/{owner}/{repo}.git /tmp/{slug}-src
   # copy only the docs subtree into the collection
   cp -R /tmp/{slug}-src/docs/. corpus/{category}/{slug}/docs/
   ```

4. **Site mirror + convert.** Only when docs exist solely as HTML with no repo or `llms.txt`. Mirror the docs section and convert to Markdown, then prune navigation chrome. This is the messiest option and a last resort.

### Discovery

Use web search and fetch to locate, in order: the canonical documentation site, the upstream source repository, and whether an `llms.txt` / `llms-full.txt` exists. Record which method you chose and why in the manifest `update_method`.

### Optional helpers

These can speed up collection but are never required, and the skill must not depend on any of them: the `llms.txt` convention, repo-to-text tools such as `repomix` or `gitingest`, `pandoc` for HTML-to-Markdown conversion, `wget`/`httrack` for mirroring, and the agent's own web search and fetch tools.

## Workflow

1. **Confirm it is a corpus, not a KB.** If the user wants a summary, switch to [kb-create](kb-create.md).
2. **Pick category and slug.** Usually `corpus/products/{slug}/` with a lowercase kebab-case slug. Add a new top-level category only if `products` does not fit.
3. **Discover the source** using web search/fetch (skip if user-provided).
4. **Choose the method** from the ladder above.
5. **Create the collection directory** `corpus/{category}/{slug}/` and acquire the docs into `corpus/{category}/{slug}/docs/`, preserving upstream structure.
6. **Normalize.** Prefer Markdown/text. Drop large binaries, images, archives, and site navigation chrome unless explicitly requested. Keep upstream filenames so internal cross-references still resolve.
7. **Write the manifest.** Copy [corpus/_template/corpus.yaml](../corpus/_template/corpus.yaml) to `corpus/{category}/{slug}/corpus.yaml` and fill in every field (see mapping below).
8. **Add a `CORPUS_INDEX.md` row** for the collection (one row per collection, not per file).
9. **Privacy scan** the acquired content (see boundaries below).
10. **Link related KBs.** If a curated entry relies on this corpus, link to it from that entry and list the `kbNNNN` ID under `related_kb`.
11. **Verify** (see below).

## Manifest Mapping Per Method

Fill `corpus.yaml` so the corpus is trustworthy and refreshable. The method determines several fields:

| Field | User-provided | `llms.txt` | Repo clone | Site mirror |
| --- | --- | --- | --- | --- |
| `source_url` | Origin if known, else `user-provided` | The `llms*.txt` URL | Repo URL | Docs site URL |
| `version` | Version the user states, else date | Site version if shown | Tag/branch/commit cloned | Site version if shown |
| `retrieved` | Date received | Fetch date | Clone date | Mirror date |
| `update_method` | "user-provided on YYYY-MM-DD" | The fetch URL/command | The exact `git clone` + copy commands | The mirror + convert commands |

Always set `license` from the upstream project, `formats` to what landed in `docs/`, `excludes` to what you intentionally dropped, `aliases` for discovery, and `privacy` once scanned.

## Privacy And Shareability Boundaries

- Never commit secrets, tokens, signed URLs, internal hostnames, or customer data.
- Respect the upstream license; record it in `license` and do not import content whose license forbids redistribution without confirming with the user.
- Scan acquired content before finishing:

  ```bash
  rg -i "token|secret|password|credential|private key|api[_-]?key" corpus/{category}/{slug}/
  ```

- Set `privacy: verified-clean` in the manifest only after scanning, or describe any redactions.

## Refreshing An Existing Corpus

1. Re-run the recorded `update_method`.
2. Replace the contents of `docs/` with the fresh copy.
3. Bump `retrieved` and, if it changed, `version` in `corpus.yaml`.
4. Update the collection's row in `CORPUS_INDEX.md`.

## Verify

- The collection exists at `corpus/{category}/{slug}/` with a filled-in `corpus.yaml` and a populated `docs/`.
- A matching row exists in `CORPUS_INDEX.md`.
- No `kbNNNN` ID was assigned and nothing was added to `INDEX.md`.
- Run `python3 tools/validate.py` to confirm the KB side is still consistent (the corpus lives outside KB validation, so this should be unaffected).

## Completion

Report:

- The collection path and the acquisition method used.
- A rough sense of size (file count and whether it is large).
- Manifest completeness and the `CORPUS_INDEX.md` row added.
- Any privacy findings or redactions, and any related KB IDs linked.
