"""Run a data preparation command while preserving reviewed chapter files."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys


def main(command):
    if not command:
        raise SystemExit("usage: preserve-certification.py COMMAND [ARG ...]")

    data_dir = Path(__file__).resolve().parents[1] / "data"
    checkpoint = json.loads((data_dir / "chapter-certification.json").read_text())
    if command == ["--check"]:
        checked = 0
        mismatches = []
        for chapter, entry in checkpoint["chapters"].items():
            expected = entry.get("final_verification", {}).get("chapter_sha256") or entry.get("chapter_sha256")
            if not expected:
                continue
            checked += 1
            path = data_dir / f"{chapter}.json"
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                mismatches.append(chapter)
        if mismatches:
            raise SystemExit("Reviewed chapter hashes do not match the checkpoint: " + ", ".join(mismatches))
        print(f"Verified {checked} reviewed chapter hashes against the checkpoint")
        return 0

    paths = {data_dir / f"{chapter}.json" for chapter in checkpoint["chapters"]}
    for book in checkpoint["preserved_previous_scope"]:
        paths.update((data_dir / book).glob("[0-9][0-9].json"))
    snapshots = {path: path.read_bytes() for path in paths}

    try:
        return subprocess.call(command)
    finally:
        restored = []
        for path, content in sorted(snapshots.items()):
            if not path.is_file() or path.read_bytes() != content:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
                restored.append(str(path.relative_to(data_dir)))
        if restored:
            print("Preserved reviewed chapters:", ", ".join(restored), flush=True)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
