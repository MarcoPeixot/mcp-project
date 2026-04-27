import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.dimension = dim
        self.texts: list[str] = []

    def _to_float32_matrix(self, embedding: list[float]) -> np.ndarray:
        if len(embedding) != self.dimension:
            raise ValueError(
                f"Embedding dimension mismatch. Expected {self.dimension}, got {len(embedding)}."
            )

        return np.array([embedding], dtype="float32")

    def add(self, embedding: list[float], text: str):
        self.index.add(self._to_float32_matrix(embedding))
        self.texts.append(text)

    def search(self, embedding: list[float], k: int = 3):
        if k <= 0:
            raise ValueError("k must be greater than zero.")

        if not self.texts:
            return []

        search_k = min(k, len(self.texts))
        distances, indices = self.index.search(
            self._to_float32_matrix(embedding), search_k
        )

        return [self.texts[i] for i in indices[0] if i != -1]
