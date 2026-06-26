# Corpus Index

Discovery index for full documentation collections under [corpus/](corpus/). Each row is **one corpus collection**, not one source file.

This is the corpus counterpart to [INDEX.md](INDEX.md):

- `INDEX.md` lists curated `kbNNNN` knowledge entries.
- `CORPUS_INDEX.md` lists complete source documentation collections.

See [corpus/README.md](corpus/README.md) for what a corpus is and how to add one.

## Search Tips

```bash
rg -i "<term>" CORPUS_INDEX.md        # find a corpus collection by name, description, or aliases
rg -i "<term>" corpus/                # full-text search across all corpus docs
rg -i "<term>" corpus/products/helm/  # search within one collection
ls corpus/                            # list corpus categories
ls corpus/products/                   # list product collections
```

## How Agents Should Use This

1. Search `INDEX.md` and `kb/` for curated guidance first.
2. Search `CORPUS_INDEX.md` and `corpus/` for full source documentation.
3. If a KB entry references a corpus, follow that reference for deeper product detail.
4. If no KB entry matches but corpus material does, answer from the corpus and make clear it is source documentation, not curated KB guidance.
5. If KB guidance and corpus docs conflict, prefer the KB for local conventions and cite the corpus for upstream behavior.

## Collections

| Collection | Description | Version | Retrieved | Path | Related KB |
| --- | --- | --- | --- | --- | --- |
| _none yet_ | Add a row when you import a corpus collection. | | | | |
