"""Verify the permanent NT baseline and the append-only verse revision ledger."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


CHAPTERS = "baseline/v0.93-reviewed-nt.sha256"
RECORDS = "baseline/v0.93-reviewed-nt-records.sha256"
LEDGER = "baseline/revisions.json"
PINS = {
    CHAPTERS: "f087c5a45b2eec882450b0ac6fd92a7c08d20775cdab0060d41368b7166ec6ad",
    RECORDS: "a43ffa666d9581b021484bd12f33fbb8e272a18f1a8339aac6c54825c96b9c25",
}
CHAPTER_PATH = re.compile(r"data/[a-z0-9]+/[0-9]{2}\.json")
REVISION_FIELDS = {"chapter", "verses", "before_sha256", "after_sha256", "reason", "pull_request"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(content):
    return hashlib.sha256(content).hexdigest()


def read(root, path):
    file = root / path
    require(file.resolve() == file and file.is_file(), f"Missing or symlinked protected file: {path}")
    return file.read_bytes()


def manifest(root, filename):
    content = read(root, filename)
    require(digest(content) == PINS[filename], f"Immutable manifest digest mismatch: {filename}")
    return {path: sha for sha, path in (line.split("  ", 1) for line in content.decode().splitlines())}


def revisions(content):
    entries = json.loads(content)
    require(isinstance(entries, list), "Revision ledger must be a JSON array")
    return entries


def apply_revisions(entries, expected):
    seen = set()
    for entry in entries:
        require(isinstance(entry, dict) and entry.keys() == REVISION_FIELDS, "Invalid revision fields")
        chapter = entry["chapter"]
        before, after = entry["before_sha256"], entry["after_sha256"]
        verses, pr = entry["verses"], entry["pull_request"]
        require(isinstance(chapter, str) and chapter in expected, f"Unknown revision chapter: {chapter}")
        require(isinstance(after, str) and re.fullmatch(r"[0-9a-f]{64}", after), f"Invalid SHA-256: {chapter}")
        require(before == expected[chapter] and after != before, f"Broken revision hash chain: {chapter}")
        require(isinstance(verses, list) and verses and all(type(v) is int and v > 0 for v in verses)
                and verses == sorted(set(verses)), f"Invalid revision verse list: {chapter}")
        require(type(pr) is int and pr > 0 and (pr, chapter) not in seen, f"Invalid or duplicate PR: {chapter}")
        require(isinstance(entry["reason"], str) and entry["reason"].strip(), f"Missing rationale: {chapter}")
        seen.add((pr, chapter))
        expected[chapter] = after


def compare_verses(before, after, entry):
    before, after = json.loads(before), json.loads(after)
    old_verses, new_verses = before.pop("verses"), after.pop("verses")
    require(before == after and [v["v"] for v in old_verses] == [v["v"] for v in new_verses],
            f"Revision changed chapter metadata or verse inventory: {entry['chapter']}")
    changed = sorted(old["v"] for old, new in zip(old_verses, new_verses) if old != new)
    require(changed == entry["verses"], f"Revision verse scope mismatch: {entry['chapter']}: {changed}")


def git_blob(root, ref, path):
    return subprocess.check_output(["git", "-C", root, "show", f"{ref}:{path}"])


def check_append(root, entries, ref, pr):
    ledger_exists = subprocess.run(
        ["git", "-C", root, "cat-file", "-e", f"{ref}:{LEDGER}"], capture_output=True
    ).returncode == 0
    if not ledger_exists:
        require(not entries, "The revision ledger must start empty")
        return
    previous = revisions(git_blob(root, ref, LEDGER))
    require(entries[:len(previous)] == previous, "Existing revision records must be preserved in order")
    additions = entries[len(previous):]
    require(len({entry["chapter"] for entry in additions}) == len(additions),
            "Record at most one revision per chapter in this change")
    for entry in additions:
        require(pr is None or entry["pull_request"] == pr, "Revision must reference this pull request")
        chapter = entry["chapter"]
        before, after = git_blob(root, ref, chapter), read(root, chapter)
        require(digest(before) == entry["before_sha256"], f"Revision starts from the wrong bytes: {chapter}")
        compare_verses(before, after, entry)


def gh_api(endpoint, *args):
    return subprocess.check_output(["gh", "api", endpoint, *args])


def check_approvals(entries, repo):
    # Bind each entry and its byte-level result to the final approved PR head.
    for pr in sorted({entry["pull_request"] for entry in entries}):
        pull = json.loads(gh_api(f"repos/{repo}/pulls/{pr}"))
        require(pull["merged"] and pull["base"]["ref"] == "main", f"Revision PR #{pr} must be merged to main")
        sha = pull["head"]["sha"]
        comments = json.loads(gh_api(f"repos/{repo}/issues/{pr}/comments", "--paginate", "--slurp"))
        owner = repo.split("/", 1)[0].lower()
        require(any(comment["user"]["login"].lower() == owner
                    and comment["body"].strip() == f"Approve reviewed NT revision {sha}"
                    for page in comments for comment in page),
                f"Missing repository owner approval for PR #{pr} at {sha}")

        def approved_file(path):
            return gh_api(f"repos/{repo}/contents/{path}?ref={sha}", "-H", "Accept: application/vnd.github.raw+json")

        approved_entries = revisions(approved_file(LEDGER))
        for entry in (entry for entry in entries if entry["pull_request"] == pr):
            chapter = entry["chapter"]
            require(entry in approved_entries and digest(approved_file(chapter)) == entry["after_sha256"],
                    f"Revision differs from approved PR #{pr}: {chapter}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--against", help="Compare the ledger and changed verse scope to this Git commit")
    parser.add_argument("--pull-request", type=int, help="Require new records to reference this pull request")
    parser.add_argument("--approval-repo", help="Verify merged PR approvals through GitHub before deployment")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        for path, sha in manifest(root, RECORDS).items():
            require(digest(read(root, path)) == sha, f"Protected record digest mismatch: {path}")
        expected = manifest(root, CHAPTERS)
        actual = {path.relative_to(root).as_posix() for path in root.glob("data/*/*.json")
                  if CHAPTER_PATH.fullmatch(path.relative_to(root).as_posix())}
        require(actual == expected.keys(),
                f"Chapter inventory mismatch. Missing: {sorted(expected.keys() - actual)}. "
                f"Unexpected: {sorted(actual - expected.keys())}")
        entries = revisions(read(root, LEDGER))
        apply_revisions(entries, expected)
        mismatches = [path for path, sha in expected.items() if digest(read(root, path)) != sha]
        require(not mismatches, "Protected chapter digest mismatch: " + ", ".join(mismatches))
        if args.against:
            check_append(root, entries, args.against, args.pull_request)
        if args.approval_repo:
            check_approvals(entries, args.approval_repo)
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Reviewed NT integrity check failed: {error}\n")
    print(f"Reviewed NT integrity verified for {len(expected)} chapter files and {len(entries)} recorded revisions")


if __name__ == "__main__":
    main()
