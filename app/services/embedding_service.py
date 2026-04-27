import os

from openai import OpenAI

class EmbeddingService:
    def __init__(self) -> None:
        self.client: OpenAI | None = None

    def _get_client(self) -> OpenAI:
        if self.client is not None:
            return self.client

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required for semantic search features.")

        self.client = OpenAI(api_key=api_key)
        return self.client

    def embed(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("Text for embedding must not be empty.")

        response = self._get_client().embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
        return response.data[0].embedding
