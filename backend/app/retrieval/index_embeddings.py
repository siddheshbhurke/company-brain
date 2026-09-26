from app.core.database import SessionLocal
from app.models import DocumentChunk
from app.retrieval.embeddings import generate_embeddings


BATCH_SIZE = 50


def index_embeddings():

    db = SessionLocal()

    try:

        chunks = (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.embedding.is_(None)
            )
            .order_by(DocumentChunk.id)
            .all()
        )

        print(
            f"Chunks requiring embeddings: {len(chunks)}"
        )

        if not chunks:
            print("All chunks already have embeddings.")
            return

        for start in range(
            0,
            len(chunks),
            BATCH_SIZE
        ):

            batch = chunks[
                start:start + BATCH_SIZE
            ]

            texts = [
                chunk.content
                for chunk in batch
            ]

            embeddings = generate_embeddings(
                texts,
                task_type="RETRIEVAL_DOCUMENT",
            )

            for chunk, embedding in zip(
                batch,
                embeddings
            ):
                chunk.embedding = embedding

            db.commit()

            print(
                f"Embedded "
                f"{start + len(batch)}/"
                f"{len(chunks)} chunks"
            )

        print(
            "Embedding indexing completed."
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    index_embeddings()
