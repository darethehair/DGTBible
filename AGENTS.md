# DGTBible alignment certification

Read `data/chapter-certification.json` and recent Git history before making changes. Preserve Matthew's earlier review and all completed chapter work. Use the existing checkout and task branch. Reconcile any committed corrections missing from the checkpoint before resuming.

- Finish Mark 1–16, including final verification of corrected chapters, then proceed through the remaining New Testament books in canonical order. Use the checkpoint to resume without repeating completed work.
- Read the actual Greek and DGT English locally and review every verse in both directions. Check missing links, unused Greek with an English rendering, repeated words linked to the wrong occurrence, broad hover spans, incorrect supplied labels, and grammatical words. Preserve legitimate supplied English and Greek elements with no separate English rendering.
- Preserve the Greek and DGT wording. Use scripts to surface candidates and check reconstruction, source IDs and regressions. Decide links using bilingual judgment. An automated pass alone cannot certify a chapter. Record heuristic false positives explicitly and resolve unexplained failures.
- Before any automated repair or regeneration, protect checkpointed chapter files and the preserved Matthew scope. Use `python3 scripts/preserve-certification.py <command> [args...]` for commands that might rewrite reviewed chapter data. Run an intentional, targeted, bilingual correction directly and review its diff. Check that deployment preparation retains the same reviewed chapter bytes before publishing.
- Keep `data/chapter-certification.json` current. Record correction scope and evidence, verification results, the next review chapter, and any outstanding final verification. Record deployment evidence separately and certify only once the verified chapter content is confirmed deployed.
- Commit durable corrections and checkpoint updates on the task branch where supported. Continue without waiting between chapters. If blocked by resources, leave an exact resume point and identify the remaining checks.

## Publish each verified book

- Prepare one release per book after its final bilingual verification. Increment the visible `APP_VERSION` in `app.js` and the service worker's `CACHE` identifier in `sw.js` using their existing sequences. Commit both with the release checkpoint.
- Run the Pages validation steps on a temporary copy. Verify that deployment preparation preserves reviewed chapter files, and record their SHA-256 hashes in the checkpoint.
- Publish to GitHub. Use a pull request into `main` when required by branch protection or the environment. Verify the release commit is on `main` and monitor the GitHub Pages workflow through completion.
- Confirm the live app shows the new version and the public chapter files match the verified hashes. Record the deployed commit and workflow run in the checkpoint before marking the book certified. Keep that evidence on `main`.
- Continue with the next book in canonical order without waiting for routine approval. If permissions prevent a push or merge, preserve the release commits and explain exactly what a maintainer needs to push, approve, or merge. Continue independent review work while publication is blocked.
