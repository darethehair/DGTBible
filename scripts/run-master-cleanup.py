#!/usr/bin/env python3
"""Run repeatable conservative NT alignment cleanup and persist a review checkpoint."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAFE_PASSES = [
    "scripts/sanitize-broad-phrase-alignments.py",
    "scripts/repair-master-exact-unlinked.py",
    "scripts/retarget-master-exact-wrong.py",
]
MAX_PASSES = 4

def run(script, preserve_reviewed=False):
    print(f"\n=== {script} ===", flush=True)
    command = ["python", script]
    if preserve_reviewed:
        command = ["python", "scripts/preserve-certification.py", *command]
    subprocess.run(command, cwd=ROOT, check=True)

def changed_data_files():
    p = subprocess.run(
        ["git", "diff", "--name-only", "--", "data"],
        cwd=ROOT, check=True, text=True, capture_output=True
    )
    return {x for x in p.stdout.splitlines() if x.strip()}

before = changed_data_files()
for pass_no in range(1, MAX_PASSES + 1):
    start = changed_data_files()
    print(f"\n### conservative cleanup pass {pass_no}/{MAX_PASSES}", flush=True)
    for script in SAFE_PASSES:
        run(script, preserve_reviewed=True)
    end = changed_data_files()
    if end == start:
        print("No additional data changes in this pass; fixed point reached.", flush=True)
        break

run("scripts/master-nt-review.py")
summary_path = ROOT / "master-review" / "summary.json"
summary = json.loads(summary_path.read_text(encoding="utf8"))
checkpoint = {
    "schema": 1,
    "purpose": "Persistent checkpoint for the conservative full-NT master alignment cleanup",
    "summary": summary,
}
out = ROOT / "data" / "master-review-progress.json"
out.write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
print("\nPersistent checkpoint:")
print(json.dumps(summary, ensure_ascii=False, indent=2))
print(f"Data files changed this run: {len(changed_data_files() - before)}")
