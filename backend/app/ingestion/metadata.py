from pathlib import Path
import hashlib
from datetime import datetime


def calculate_file_hash(path: Path) -> str:

    sha256 = hashlib.sha256()

    with open(path, "rb") as file:

        for block in iter(
            lambda: file.read(1024 * 1024),
            b""
        ):
            sha256.update(block)

    return sha256.hexdigest()


def build_metadata(
    path: Path,
    content_hash: str
) -> dict:

    return {
        "filename": path.name,
        "extension": path.suffix.lower(),
        "source_path": str(path),
        "content_hash": content_hash,
        "ingested_at": datetime.utcnow().isoformat(),
    }
