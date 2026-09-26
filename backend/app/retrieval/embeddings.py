from google import genai
from google.genai import types

from app.core.config import settings


MODEL_NAME = "gemini-embedding-001"
OUTPUT_DIMENSIONALITY = 1536


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def generate_embedding(
    text: str,
    task_type: str = "RETRIEVAL_DOCUMENT",
) -> list[float]:

    response = client.models.embed_content(
        model=MODEL_NAME,
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=OUTPUT_DIMENSIONALITY,
            task_type=task_type,
        ),
    )

    return response.embeddings[0].values


def generate_embeddings(
    texts: list[str],
    task_type: str = "RETRIEVAL_DOCUMENT",
) -> list[list[float]]:

    if not texts:
        return []

    response = client.models.embed_content(
        model=MODEL_NAME,
        contents=texts,
        config=types.EmbedContentConfig(
            output_dimensionality=OUTPUT_DIMENSIONALITY,
            task_type=task_type,
        ),
    )

    return [
        embedding.values
        for embedding in response.embeddings
    ]
