"""Package the tagged NT baseline for standalone use and data reuse."""

import argparse
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
TAG = "v0.93-reviewed-nt"
PWA_FILES = ["index.html", "app.js", "style.css", "sw.js", "manifest.webmanifest", "icons/icon.svg"]
CHAPTERS = ROOT / f"baseline/{TAG}.sha256"
RECORDS = ROOT / f"baseline/{TAG}-records.sha256"


def package(output):
    output.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, ROOT / "scripts/check-reviewed-baseline.py"], check=True)
    data_files = [line.split("  ", 1)[1] for manifest in (CHAPTERS, RECORDS)
                  for line in manifest.read_text().splitlines()]
    books = [Path(path).parent for path in data_files if path.endswith("/manifest.json")]
    data_files.extend(str(book / name) for book in books for name in ("paragraphs.json", "editorial-notes.json"))
    files = sorted(set(data_files + [
        str(CHAPTERS.relative_to(ROOT)), str(RECORDS.relative_to(ROOT)),
        "baseline/revisions.json", "baseline/README.md", "NOTICE.md",
    ]))
    for name, members in [("pwa", files + PWA_FILES), ("data", files)]:
        destination = output / f"DGTBible-{TAG}-{name}.zip"
        with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
            for member in sorted(members):
                info = ZipInfo(member)
                info.external_attr = 0o100644 << 16
                archive.writestr(info, (ROOT / member).read_bytes(), compress_type=ZIP_DEFLATED)
        with TemporaryDirectory() as scratch, ZipFile(destination) as archive:
            archive.extractall(scratch)
            subprocess.run([sys.executable, ROOT / "scripts/check-reviewed-baseline.py",
                            "--root", scratch], check=True)
    for manifest in (CHAPTERS, RECORDS):
        shutil.copyfile(manifest, output / manifest.name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    package(parser.parse_args().output)
