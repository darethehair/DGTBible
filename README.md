# DGTBible

Original-language New Testament PWA featuring the **DGT — Direct Greek Translation**.

## Open the app

**[Launch DGTBible on GitHub Pages](https://darethehair.github.io/DGTBible/)**

Read directly in your browser or use its **Install app** or **Add to Home Screen** option where supported. For a local static copy, run `python3 -m http.server 8000` from the app directory and open `http://localhost:8000/`. See the [reviewed baseline guide](baseline/README.md) for release downloads and checksum verification.

## Current edition

- Installable static PWA with no API key or runtime AI cost.
- **All 27 New Testament books are complete** with SBLGNT Greek, transliteration, literal Greek-order English, fresh DGT English, and linked alignment data.
- **SBLGNT** Greek base text, licensed under CC BY 4.0.
- DGT English translation stored locally alongside each verse.
- Linked Greek/transliteration/literal/DGT highlighting across the completed books, assisted by pinned STEPBible TAGNT word data.
- Study, Chapter, and Compact reading modes with remembered layer preferences.
- Light, dark, and system themes with a remembered preference.
- Amber daggers beside selected textually disputed passages open manuscript notes in all three reading modes.
- Direct verse lookup (`John 1:18`) and shareable URL hashes (`#John.1.18`).
- Offline cache through a service worker; core Scripture and alignment data are local and do not depend on STEPBible at runtime.
- GitHub Pages workflow included.

## Recorded audio

Open **Recorded audio** and press **Play**. Study defaults to the displayed verse. Chapter and Compact default to the displayed chapter. You can also enter a verse range, a chapter range, a book, or a comma-separated selection.

The player shows which verses are available for the selected narrator. It highlights the narrated verse, can scroll it into view, and remembers narrator, speed, and auto-scroll preferences. Unrecorded verses are skipped and counted. Playback requires an Ogg Opus-capable browser and a network connection for uncached recordings.

The English female recordings for John 1 were generated with [Pocket TTS](https://github.com/kyutai-labs/pocket-tts), developed by Kyutai. Recordings are served by the [DGTBible audio library](https://github.com/darethehair/DGTBible-Audio).

## Translation method

DGT is a fresh English translation created directly from the original-language text with AI assistance. It aims to preserve wording, structure, repetition, and theological vocabulary while remaining readable English. Difficult or textually significant readings should be checked against modern critical editions and manuscript evidence rather than silently normalized.

The embedded Greek text is the **SBL Greek New Testament (SBLGNT)**, a modern critically edited Greek New Testament. SBLGNT is © 2010 Society of Biblical Literature and Logos Bible Software and is licensed under **CC BY 4.0**.

For word-level alignment and lexical metadata, DGTBible also uses a pinned authoring snapshot derived from **STEPBible TAGNT**, likewise under **CC BY 4.0**. The snapshot is stored locally in this repository, so the app does not depend on STEPBible being online. See [source notices](NOTICE.md) for exact revisions, attribution, and license links.

DGT translation and notes are separate original project content.

## Status

The complete New Testament is available as a reading and study edition. The [reviewed baseline](baseline/README.md) documents the release and chapter review evidence.

DGT is an independently produced study translation with AI assistance. It has no formal peer review as a critical edition.

## Data validation

GitHub Actions validates the generated New Testament data before deployment. The checks include chapter/verse coverage, alignment reconstruction, source-ID integrity, semantic alignment sanity, structural hover breadth, and corpus-level checks for suspicious missing or overly broad links.

Reviewed exceptions and precision repairs are stored explicitly so later regeneration does not silently discard earlier human-reviewed decisions. Ambiguous cases are preferred as unlinked or explicitly supplied English rather than being forced into misleading Greek-word links.

## Alignment safety

Generated DGT alignments publish only high-confidence lexical links. Deployment also applies reviewed alignment overrides and runs a corpus-wide critical lexical-sanity gate that checks for uniquely plausible missing or wrong lexical links. Ambiguous helper words or uncertain mappings are deliberately left unlinked rather than guessed. John 4–10 was generated and audited as a 366-verse calibration batch. John 11–21 was then generated as a 400-verse completion batch at 86.6% high-confidence DGT token coverage, with 1,242 deliberately unlinked tokens and zero high-risk mappings. Source-variant exceptions are handled explicitly rather than by silent positional fallback.

Development planning is tracked in [ROADMAP.md](ROADMAP.md).
