from sqlalchemy import select

from app.core.database import SessionLocal
from app.models import DocumentChunk
from app.retrieval.embeddings import generate_embedding


def semantic_search(
    query: str,
    top_k: int = 5,
):

    query_embedding = generate_embedding(
        query,
        task_type="RETRIEVAL_QUERY",
    )

    db = SessionLocal()

    try:

        distance = DocumentChunk.embedding.cosine_distance(
            query_embedding
        ).label("distance")

        statement = (
            select(
                DocumentChunk,
                distance,
            )
            .where(
                DocumentChunk.embedding.is_not(None)
            )
            .order_by(distance)
            .limit(top_k)
        )

        results = db.execute(statement).all()

        return results

    finally:
        db.close()


if __name__ == "__main__":

    query = (
        "What is the approval requirement "
        "for a 75000 INR refund?"
    )

    results = semantic_search(
        query,
        top_k=5,
    )

    print()
    print("=" * 70)
    print("COMPANY BRAIN SEMANTIC SEARCH")
    print("=" * 70)
    print()
    print("QUERY:")
    print(query)
    print()

    for rank, (chunk, distance) in enumerate(
        results,
        start=1
    ):

        print("-" * 70)
        print(f"RESULT {rank}")
        print(f"Chunk ID : {chunk.id}")
        print(f"Distance : {distance:.4f}")
        print()
        print(chunk.content[:1000])
        print()
