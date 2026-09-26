from pathlib import Path

from sqlalchemy.orm import Session

from app.ingestion.parsers import parse_file
from app.ingestion.chunker import chunk_text
from app.ingestion.metadata import (
    calculate_file_hash,
    build_metadata,
)

from app.models import Document, DocumentChunk


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".json",
    ".csv",
}


def detect_source_type(path: Path) -> str:

    name = path.name.lower()

    if "policy" in name:
        return "policy"

    if "sop" in name:
        return "sop"

    if path.suffix.lower() == ".csv":
        return "process_event_log"

    if "ticket" in name:
        return "support_ticket"

    if "email" in name:
        return "email"

    if "slack" in name:
        return "slack"

    if path.parent.name == "company":
        return "structured_company_data"

    return "unknown"


def ingest_file(
    db: Session,
    path: Path
) -> Document:

    path = path.resolve()

    content = parse_file(path)

    content_hash = calculate_file_hash(path)

    metadata = build_metadata(
        path,
        content_hash
    )

    source_type = detect_source_type(path)

    existing = (
        db.query(Document)
        .filter(
            Document.content_hash == content_hash
        )
        .first()
    )

    if existing:
        print(
            f"[SKIPPED] {path.name} "
            f"(already ingested)"
        )
        return existing

    document = Document(
        title=path.stem,
        source_type=source_type,
        source_uri=str(path),
        content_hash=content_hash,
        version="1.0",
        is_active=True,
    )

    db.add(document)
    db.flush()

    chunks = chunk_text(content)

    for index, chunk in enumerate(chunks):

        document_chunk = DocumentChunk(
            document_id=document.id,
            chunk_index=index,
            content=chunk,
            metadata_json={
                **metadata,
                "chunk_index": index,
            },
        )

        db.add(document_chunk)

    db.commit()
    db.refresh(document)

    return document


def ingest_directory(
    db: Session,
    directory: Path
):

    results = []

    for path in sorted(directory.rglob("*")):

        if not path.is_file():
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:

            document = ingest_file(
                db,
                path
            )

            results.append(document)

            print(
                f"[INGESTED] "
                f"{path.name} "
                f"-> Document ID {document.id}"
            )

        except Exception as exc:

            db.rollback()

            print(
                f"[FAILED] "
                f"{path.name}: {exc}"
            )

    return results
