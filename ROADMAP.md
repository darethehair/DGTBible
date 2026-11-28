# DGTBible development roadmap

This is the shared roadmap for the maintainer, Codex, and ChatGPT. Consult it when planning work and record agreed changes here. See the [README](README.md) for the released app and the [reviewed NT baseline guide](baseline/README.md) for the safeguards that apply to development.

## Reading statistics
- Add a compact upper-right word-count display.
- Verse view: Greek and DGT English word counts for the current verse.
- Chapter / Compact view: verse count plus total Greek and DGT English word counts for the chapter.
- Whole-book view: book verse count plus total Greek and DGT English word counts.
- Count real SBLGNT source tokens and displayed DGT word tokens, excluding punctuation and synthetic alignment artifacts.
- Possible later expansion: English/Greek word ratio, unique Greek lemmas, vocabulary statistics, and a richer statistics popover.

## Display themes (implemented)

Light, dark, and system settings are available, with the reader's preference saved locally. Alignment highlighting, selected-word emphasis, notes, and accessible contrast remain design requirements across themes.

## Chronological reading plans and progress tracking
- Add automated chronological-order reading plans, beginning with a **90-day New Testament plan** and leaving room for other durations later.
- Divide the plan into dated daily portions and clearly show what must be read **today**, what is completed, and what remains to stay on schedule.
- Let the reader mark a day's portion **complete** with a simple click or tap. Preserve progress locally so the static PWA works offline without an account.
- Highlight the currently assigned reading portion in chapter/compact reading views so the user can read directly through the plan rather than merely seeing a checklist.
- Show useful schedule status such as days completed, today's assignment, overdue portions, ahead/behind status, and the next reading.
- Design progress data so a future optional sync/account layer could be added without changing the reading-plan model.
- Future enhancement: **read-aloud / text-to-speech** for the assigned daily portion, with highlighting that follows the spoken text if practical.

## Greek word / lemma explorer
- Keep hover as the lightweight Greek ↔ English alignment interaction.
- Make a Greek-word click open lexical details: surface form, transliteration, lemma, gloss, morphology, and the aligned DGT rendering.
- Add “Find all occurrences” for the Greek lemma across the completed corpus, with an optional exact-inflected-form filter.
- Show every matching book/verse with the Greek occurrence and corresponding DGT English rendering highlighted.
- Summarize how a Greek lemma is rendered across DGT (for example, translation wording + occurrence counts).
- Build a precomputed local corpus index so concordance searches remain fast and work offline.
- Later consider the inverse English workflow: click an English word to find the Greek lemmas translated by that wording.

## Audio narration

- Plan a hybrid audio Bible with pregenerated verse recordings for slower devices and optional live neural TTS for faster devices.
- Use PocketTTS as the initial English narration engine. Keep voice choice and pronunciation review part of the recording workflow, with corrections stored separately from the Scripture text.
- Keep English male, English female, custom voice, and original-language Greek as separate narrator slots. Track the source text, voice, model, pronunciation dictionary, encoding, and audio checksum for each recording.
- Preserve the planned read-aloud integration for chronological reading assignments, with synchronized highlighting where practical.

## Long-term Old Testament expansion

The eventual application will support three corpora:

| Corpus | Textual tradition |
| --- | --- |
| **DGT-NT** | Greek New Testament |
| **DGT-MT** | Masoretic Old Testament in Hebrew and Aramaic |
| **DGT-LXX** | Septuagint Old Testament in Greek |

Treat the Masoretic Text (MT) and Septuagint (LXX) as independent, first-class textual traditions. Each OT corpus should provide four layers, as the NT does:

1. Original-language text in Hebrew and Aramaic for MT and Greek for LXX.
2. Transliteration.
3. Literal English rendering.
4. Independent DGT English translation from that corpus's own source text.

Preserve the wording, meaning, and textual distinctions of each tradition in both English layers. Keep each corpus's translation, alignment, and notes tied to its own source. Both OT corpora should support interactive bidirectional word alignment, concordance searches, textual notes, and eventual audio narration.

### Reading and study across traditions

- Switch between MT and LXX and compare corresponding passages side by side while retaining each passage's native reference.
- Map different chapter and verse numbering, book names and organization, additions, and omissions. Allow passages to correspond to multiple ranges or have no documented counterpart.
- Link NT quotations to relevant passages in both OT traditions and identify the corpus for each link.
- Support right-to-left Hebrew and Aramaic display alongside left-to-right transliteration and English. Include Hebrew morphology in lexical study, concordances, and alignment.

### Design considerations for new work

- **References** should allow a corpus and its native numbering scheme to disambiguate book, chapter, and verse. Preserve existing NT references and shareable links.
- **Audio organization** should be able to distinguish recordings by corpus, native reference, narrator, and source version.
- **Concordances** should support corpus- and language-specific indexes, with an explicit corpus scope for searches and cross-corpus results.
- **Chronological reading** should be able to assign corpus-specific passages and track progress against the selected plan, even where book order and versification differ.

This is long-term planning. Begin OT translation or major architectural work only when separately authorized. The reviewed NT baseline and its translation and alignment safeguards continue to govern all current work.
