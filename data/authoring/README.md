# DGT authoring format

Existing DGT TSV files may contain the legacy three columns:

```
DGT<TAB>chapter:verse<TAB>plain DGT translation
```

For **1 Corinthians 5 onward**, translation and alignment are authored together. Each row must contain a fourth column: a JSON array with exactly one source-ID list for each whitespace-delimited DGT token.

```
DGT<TAB>5:1<TAB>Example good news text.<TAB>[["w1"],["w2"],["w3","w4"],["w5"]]
```

Rules:

- The fourth-column array length must equal the number of DGT whitespace tokens.
- IDs are the Greek source IDs produced from the SBLGNT/STEP source mapping (for example `w7`).
- One Greek source may intentionally appear on several English tokens, e.g. `good` and `news` can both carry the same ID.
- One English token may carry multiple Greek IDs when it renders a Greek phrase.
- Use `[]` only when a DGT token is intentionally not tied to a Greek source.
- The build validates every authored ID against the verse source and marks these links `confidence: "authored"`.
- 1 Corinthians 1–4 remain compatible with the legacy matcher so the already-reviewed material is not regenerated destructively.

This makes the alignment part of translation intent. Heuristic alignment and lexical scanners remain QA/repair tools for legacy material, not the primary source of alignment for new translation.
