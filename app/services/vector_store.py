import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add(self, embedding: list[float], text: str):
        self.index.add(np.array([embedding]).astype("float32"))
        self.texts.append(text)

    def search(self, embedding: list[float], k: int = 3):
        distances, indices = self.index.search(
            np.array([embedding]).astype("float32"), k
        )

        return [self.texts[i] for i in indices[0]]