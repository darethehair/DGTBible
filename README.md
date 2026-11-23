# DGTBible

Experimental original-language Bible PWA with the **DGT — Direct Greek Translation**.

## Current prototype

- Installable static PWA; no API key and no runtime AI cost.
- John 1–21, 1–3 John, Jude, 1–2 Peter, James, Hebrews, and Romans are complete with SBLGNT Greek, literal Greek-order English, fresh DGT English, and selective translation notes.
- **SBLGNT** Greek base text, licensed under CC BY 4.0.
- DGT English translation stored locally alongside each verse.
- Linked Greek/transliteration/literal/DGT highlighting across the completed books, assisted by pinned STEPBible TAGNT word data.
- Study mode and continuous chapter-reading mode with remembered layer preferences.
- Direct verse lookup (`John 1:18`) and shareable URL hashes (`#John.1.18`).
- Offline cache through a service worker; core Scripture and alignment data are local and do not depend on STEPBible at runtime.
- GitHub Pages workflow included.


## Roadmap

### Reading statistics
- Add a compact upper-right word-count display.
- Verse view: Greek and DGT English word counts for the current verse.
- Chapter / Compact view: verse count plus total Greek and DGT English word counts for the chapter.
- Whole-book view: book verse count plus total Greek and DGT English word counts.
- Count real SBLGNT source tokens and displayed DGT word tokens, excluding punctuation and synthetic alignment artifacts.
- Possible later expansion: English/Greek word ratio, unique Greek lemmas, vocabulary statistics, and a richer statistics popover.

### Greek word / lemma explorer
- Keep hover as the lightweight Greek ↔ English alignment interaction.
- Make a Greek-word click open lexical details: surface form, transliteration, lemma, gloss, morphology, and the aligned DGT rendering.
- Add “Find all occurrences” for the Greek lemma across the completed corpus, with an optional exact-inflected-form filter.
- Show every matching book/verse with the Greek occurrence and corresponding DGT English rendering highlighted.
- Summarize how a Greek lemma is rendered across DGT (for example, translation wording + occurrence counts).
- Build a precomputed local corpus index so concordance searches remain fast and work offline.
- Later consider the inverse English workflow: click an English word to find the Greek lemmas translated by that wording.

## Translation method

DGT is a fresh English translation created directly from the original-language text with AI assistance. It aims to preserve wording, structure, repetition, and theological vocabulary while remaining readable English. Difficult or textually significant readings should be checked against modern critical editions and manuscript evidence rather than silently normalized.

The embedded Greek text is the **SBL Greek New Testament (SBLGNT)**, a modern critically edited Greek New Testament. SBLGNT is © 2010 Society of Biblical Literature and Logos Bible Software and is licensed under **CC BY 4.0**.

For word-level alignment and lexical metadata, DGTBible also uses a pinned authoring snapshot derived from **STEPBible TAGNT**, likewise under **CC BY 4.0**. The snapshot is stored locally in this repository, so the app does not depend on STEPBible being online. See `NOTICE.md` for exact source revisions and attribution.

DGT translation and notes are separate original project content.

## Status

Experimental study edition; not a formally published or peer-reviewed critical edition.

## Data validation

Before deployment, GitHub Actions runs `node scripts/validate-john.mjs`. It checks chapter/verse coverage, alignment reconstruction, alignment IDs, preserved STEPBible source coverage and metadata consistency, and curated overrides. John 1:1 is stored as a protected hand-curated override in `data/john/curated-overrides.json`; after any generated alignment pass, run `node scripts/apply-curated-overrides.mjs` before validation.

The deployment also runs a semantic alignment audit that flags suspicious reuse of a Greek word ID across separated English phrases. Reviewed legitimate split phrases are kept in `data/john/semantic-audit-allowlist.json`; any new high-risk case fails CI until reviewed.

John 3 was added as the first pilot chapter generated under the structural + semantic QA pipeline before scaling to the rest of John.

## Alignment safety

Generated DGT alignments publish only high-confidence lexical links. Deployment also applies reviewed alignment overrides and runs a corpus-wide critical lexical-sanity gate that checks for uniquely plausible missing or wrong lexical links. Ambiguous helper words or uncertain mappings are deliberately left unlinked rather than guessed. John 4–10 was generated and audited as a 366-verse calibration batch. John 11–21 was then generated as a 400-verse completion batch at 86.6% high-confidence DGT token coverage, with 1,242 deliberately unlinked tokens and zero high-risk mappings. Source-variant exceptions are handled explicitly rather than by silent positional fallback.
