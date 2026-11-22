# Source Attributions

## SBL Greek New Testament (SBLGNT)

DGTBible includes Greek New Testament text from the **SBL Greek New Testament (SBLGNT)**.

SBLGNT © 2010 Society of Biblical Literature and Logos Bible Software.

Source: https://github.com/Faithlife/SBLGNT

Licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0):
https://creativecommons.org/licenses/by/4.0/

DGTBible removes SBLGNT apparatus sigla from the displayed running Greek text for readability; the underlying wording is sourced from SBLGNT.

## STEPBible TAGNT

DGTBible uses word-level data derived from the **STEPBible Translators Amalgamated Greek New Testament (TAGNT)** as an authoring aid for alignment, transliteration, lexical identity, morphology, Strong's identifiers, and context-sensitive glosses.

Data created by **STEP Bible / STEPBible.org**, based on work at Tyndale House, Cambridge.

Primary source: https://github.com/STEPBible/STEPBible-Data

License: Creative Commons Attribution 4.0 International (CC BY 4.0).

Pinned upstream revision used for the John 1–2 authoring snapshot:
`STEPBible/STEPBible-Data@5de0a47f35f0fc13dfe1430d104e5db8a4285f9c`

For manageable per-verse extraction, DGTBible used the CC BY 4.0 parsed mirror:
https://github.com/GabeBrPierce/bible-interlinear

Pinned mirror revision:
`GabeBrPierce/bible-interlinear@2076684f9200eb1b119aa7effbf58f9ec571c0ca`

The preserved John 1–2 source snapshot is stored under `data/sources/`. DGTBible does not fetch STEPBible at runtime.

The displayed Greek remains SBLGNT. Where TAGNT's NA-based main line differs from SBLGNT, DGTBible aligns the auxiliary word data to the SBLGNT wording rather than replacing the displayed text.
