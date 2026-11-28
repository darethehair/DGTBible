# DGTBible

Original-language New Testament PWA featuring the **DGT — Direct Greek Translation**.

## Open the app

**[Launch DGTBible on GitHub Pages](https://darethehair.github.io/DGTBible/)**

Install it as a PWA in a supported browser, or use it directly in the browser.

## Current edition

- Installable static PWA; no API key and no runtime AI cost.
- **All 27 New Testament books are complete** with SBLGNT Greek, literal Greek-order English, fresh DGT English, and linked alignment data.
- **SBLGNT** Greek base text, licensed under CC BY 4.0.
- DGT English translation stored locally alongside each verse.
- Linked Greek/transliteration/literal/DGT highlighting across the completed books, assisted by pinned STEPBible TAGNT word data.
- Study mode and continuous chapter-reading mode with remembered layer preferences.
- Direct verse lookup (`John 1:18`) and shareable URL hashes (`#John.1.18`).
- Offline cache through a service worker; core Scripture and alignment data are local and do not depend on STEPBible at runtime.
- GitHub Pages workflow included.

## Recorded audio

Open **Recorded audio**, enter a passage, and choose a narrator. The player starts with English female (slot 02) and shows which narrators and verses have recordings. The other slots are English male (01), custom voice (03), and original Greek (04). Narrator, speed, and auto-scroll preferences are remembered.

The player and **Go** recognize single verses (`John 1:1`), verse ranges (`John 1:1-10`), chapters (`John 1`), chapter ranges (`John 1-3`), cross-chapter ranges (`John 1:14-3:16`), books (`John`), comma-separated selections (`John 1:1-10, Romans 1:5`), and `NT` for the entire New Testament. **Go** opens the beginning of a selection. **Play** follows the selection in order. Use **‹** and **›** to move between recordings and **Hide** to collapse active controls.

Playback marks the narrated verse in Study, Chapter, or Compact mode. It follows chapter and book changes and can scroll the current verse into view. Word-level alignment still works during playback. Speed ranges from 0.5× to 2.0× with pitch preservation.

The [audio library](https://github.com/darethehair/DGTBible-Audio) serves Ogg Opus files and a small availability manifest. As of v0.94, all 51 verses of John 1 are recorded in slot 02. The app checks the library when the player opens or playback starts, and refreshes periodically while the panel is open. Audio uploads appear after the audio repository's own Pages deployment and cache refresh. This app's service worker does not precache narration. Playback requests the current verse and at most one upcoming recording.

Unrecorded verses are skipped and counted. A missing file listed in the inventory is temporarily remembered to avoid repeated requests. Temporary network failures are reported separately and can be retried. Playback keeps the selected narrator. Audio requires an Ogg Opus-capable browser and a network connection for uncached recordings.

For the browser regression test, install Playwright for Python and a Chromium browser, then run `python scripts/test-recorded-audio.py /path/to/001.opus` with a real Ogg Opus verse. Set `PLAYWRIGHT_CHROMIUM_EXECUTABLE` to use an existing Chromium binary.


## Roadmap

### Reading statistics
- Add a compact upper-right word-count display.
- Verse view: Greek and DGT English word counts for the current verse.
- Chapter / Compact view: verse count plus total Greek and DGT English word counts for the chapter.
- Whole-book view: book verse count plus total Greek and DGT English word counts.
- Count real SBLGNT source tokens and displayed DGT word tokens, excluding punctuation and synthetic alignment artifacts.
- Possible later expansion: English/Greek word ratio, unique Greek lemmas, vocabulary statistics, and a richer statistics popover.

### Display themes
- Add a **dark mode** option with a comfortable low-glare palette for extended reading.
- Preserve Greek/DGT alignment highlighting, selected-word emphasis, notes, and accessibility contrast in both light and dark themes.
- Remember the reader's theme preference locally and allow an optional follow-system setting later.

### Chronological reading plans and progress tracking
- Add automated chronological-order reading plans, beginning with a **90-day New Testament plan** and leaving room for other durations later.
- Divide the plan into dated daily portions and clearly show what must be read **today**, what is completed, and what remains to stay on schedule.
- Let the reader mark a day's portion **complete** with a simple click/tap; preserve progress locally so the static PWA works offline without an account.
- Highlight the currently assigned reading portion in chapter/compact reading views so the user can read directly through the plan rather than merely seeing a checklist.
- Show useful schedule status such as days completed, today's assignment, overdue portions, ahead/behind status, and the next reading.
- Design progress data so a future optional sync/account layer could be added without changing the reading-plan model.
- Future enhancement: **read-aloud / text-to-speech** for the assigned daily portion, with highlighting that follows the spoken text if practical.

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

DGTBible now contains the complete New Testament and is usable as a reading and study edition. Alignment quality and interface features continue to be refined through corpus-wide QA and review.

DGT is an independently produced study translation with AI assistance; it is not a formally published or peer-reviewed critical edition.

## Data validation

GitHub Actions validates the generated New Testament data before deployment. The checks include chapter/verse coverage, alignment reconstruction, source-ID integrity, semantic alignment sanity, structural hover breadth, and corpus-level checks for suspicious missing or overly broad links.

Reviewed exceptions and precision repairs are stored explicitly so later regeneration does not silently discard earlier human-reviewed decisions. Ambiguous cases are preferred as unlinked or explicitly supplied English rather than being forced into misleading Greek-word links.

## Alignment safety

Generated DGT alignments publish only high-confidence lexical links. Deployment also applies reviewed alignment overrides and runs a corpus-wide critical lexical-sanity gate that checks for uniquely plausible missing or wrong lexical links. Ambiguous helper words or uncertain mappings are deliberately left unlinked rather than guessed. John 4–10 was generated and audited as a 366-verse calibration batch. John 11–21 was then generated as a 400-verse completion batch at 86.6% high-confidence DGT token coverage, with 1,242 deliberately unlinked tokens and zero high-risk mappings. Source-variant exceptions are handled explicitly rather than by silent positional fallback.
