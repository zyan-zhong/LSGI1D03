"""Download missing source files and verify all source checksums."""

from hashlib import sha256
import json
from pathlib import Path
import shutil
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"


def checksum(path):
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def ensure_source(source):
    target = RAW / source["file"]
    expected = source["sha256"]
    if target.is_file():
        if checksum(target) != expected:
            raise ValueError(f"Checksum mismatch for {target.name}. Check the upstream version.")
        print(f"Verified {target.name}")
        return

    bundled = [RAW / name for name in source.get("bundled_parts", [])]
    partial = target.with_name(f"{target.name}.part")
    try:
        with partial.open("wb") as output:
            if bundled and all(part.is_file() for part in bundled):
                for part in bundled:
                    with part.open("rb") as stream:
                        shutil.copyfileobj(stream, output)
            else:
                with urlopen(source["download"], timeout=60) as response:
                    shutil.copyfileobj(response, output)
        if checksum(partial) != expected:
            raise ValueError(f"Checksum mismatch for recovered input {target.name}.")
        partial.replace(target)
        print(f"Restored and verified {target.name}")
    finally:
        partial.unlink(missing_ok=True)


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8"))
    for source in manifest:
        ensure_source(source)


if __name__ == "__main__":
    main()
