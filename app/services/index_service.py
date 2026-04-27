class DocumentIndexService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore(dim=1536)

    def index_document(self, text: str):
        chunks = chunk_text(text)

        for chunk in chunks:
            embedding = self.embedding_service.embed(chunk)
            self.vector_store.add(embedding, chunk)

    def query(self, query: str):
        embedding = self.embedding_service.embed(query)
        return self.vector_store.search(embedding)