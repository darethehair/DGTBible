"""Run a data preparation command while preserving reviewed chapter files."""

import json
from pathlib import Path
import subprocess
import sys


def main(command):
    if not command:
        raise SystemExit("usage: preserve-certification.py COMMAND [ARG ...]")

    data_dir = Path(__file__).resolve().parents[1] / "data"
    checkpoint = json.loads((data_dir / "chapter-certification.json").read_text())
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
