from openai import openai

client = OpenAI()

class EmbeddingService:
    def embed(self, text: str) -> list[float]:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

        