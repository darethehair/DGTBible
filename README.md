# DGTBible

Experimental original-language Bible PWA with the **DGT — Direct Greek Translation**.

## Current prototype

- Installable static PWA; no API key and no runtime AI cost.
- John 1–2 seeded with selected high-value verses as the first corpus; the schema is ready for complete chapters.
- **SBLGNT** Greek base text, licensed under CC BY 4.0.
- DGT English translation stored locally alongside each verse.
- Direct verse lookup (`John 1:18`) and shareable URL hashes (`#John.1.18`).
- Offline cache through a service worker.
- GitHub Pages workflow included.

## Translation method

DGT is a fresh English translation created directly from the original-language text with AI assistance. It aims to preserve wording, structure, repetition, and theological vocabulary while remaining readable English. Difficult or textually significant readings should be checked against modern critical editions and manuscript evidence rather than silently normalized.

The embedded Greek text is the **SBL Greek New Testament (SBLGNT)**, a modern critically edited Greek New Testament. SBLGNT is © 2010 Society of Biblical Literature and Logos Bible Software and is licensed under **CC BY 4.0**. DGT translation and notes are separate original project content.

## Status

Experimental study edition; not a formally published or peer-reviewed critical edition.
