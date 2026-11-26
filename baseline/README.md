# DGTBible v0.93 reviewed New Testament

This baseline preserves the Greek and DGT English text and alignment data for all 260 chapters in 27 books. The permanent annotated tag `v0.93-reviewed-nt` includes the manifests and integrity guard alongside the original chapter bytes.

- **232 chapters** were formally certified, with final bilingual verification, chapter hashes, and deployment evidence in the completion checkpoint.
- **28 Matthew chapters** were previously reviewed and preserved byte-for-byte. Their original certification evidence remains unrecovered.

The [completion checkpoint](https://github.com/darethehair/DGTBible/blob/31a5c5e94f683de41d98823f2731fa290a649c4c/data/chapter-certification.json) is from commit `31a5c5e94f683de41d98823f2731fa290a649c4c`. It records the original [v0.93 Pages deployment](https://github.com/darethehair/DGTBible/actions/runs/45827348231) of commit `45d7a217538d7b54ef85a6fab6ac7ac7f46989f5`, with service-worker cache `dgtbible-v103`.

## Download and verify

- The PWA ZIP contains the static app and all data it needs. Extract it, run `python3 -m http.server 8000` from the extracted directory, and open [localhost:8000](http://localhost:8000). The service worker can install and cache the corpus on localhost. Keep the included source notices with redistributed copies.
- The data ZIP contains all 260 chapters, book metadata, editorial notes, the final checkpoint, both baseline manifests, and the source notices.
- Verify downloads with `sha256sum -c SHA256SUMS`. Keep `SHA256SUMS` beside all four assets.
- Run `sha256sum -c baseline/v0.93-reviewed-nt.sha256` and `sha256sum -c baseline/v0.93-reviewed-nt-records.sha256` from an extracted archive. The annotated tag records independent digests for both manifest files.

## Intentional verse corrections

1. Open a pull request against `main`. Identify the exact verses, describe the issue, and record the bilingual reasoning. Review translation and alignment changes in both directions. Keep any unrelated formatting, wording, links, and verses intact.
2. Verify the focused semantic and structural changes locally and rehearse the Pages audit commands. Append one record per affected chapter to `baseline/revisions.json`. Each record requires `chapter` (repo-relative path such as `data/mark/01.json`), `verses` (sorted unique integers), `before_sha256` (current byte digest on main), `after_sha256` (candidate byte digest), `reason` (bilingual rationale), and `pull_request` (GitHub PR number). Keep prior entries in order. Run `python3 scripts/check-reviewed-baseline.py --against origin/main --pull-request PR_NUMBER` against the latest main.
3. The repository owner records explicit approval on the PR with an exact standalone comment `Approve reviewed NT revision FULL_HEAD_SHA`. Obtain fresh approval after changing the approved head. Merge only after the Reviewed NT integrity check passes and approval is recorded. Pages verifies each recorded approval and binds the chapter bytes and ledger entry to its approved, merged PR head.
4. For a published verse correction, increment `APP_VERSION` and the service-worker cache using their established sequences. Confirm that Pages succeeds and the public payload hashes match the approved contents. Add the Pages run and live verification evidence to the same PR conversation. The baseline checkpoint records the original certification. Record revision approval and deployment evidence separately in the PR.
5. Keep both manifests, the checkpoint, and the baseline tag and release as permanent records. Retain previously approved ledger entries and approval comments. A reversal needs a new approved revision. Use `python3 scripts/preserve-certification.py COMMAND [ARGS...]` around automated authoring scripts to preserve the current chapter bytes.

Local preflight uses `python3 scripts/preserve-certification.py --check` or the checker with `--against origin/main` for a pending PR. For an independent check, fetch the baseline tag and run its checker against the checkout. GitHub Actions pins annotated tag object `2e85deb2b58bf6684424ac53dabe446fa2ffd2e7` and runs its checker on pull requests and before Pages upload. It verifies the immutable chapter manifest, final checkpoint, book routing manifests, chapter inventory, revision hash chain, and changed verse scope. Keep the baseline tag protected against update and deletion by a GitHub tag ruleset or repository immutable releases. Require the Reviewed NT integrity job and maintainer review of changes to guard or workflow files in the main branch rules.
