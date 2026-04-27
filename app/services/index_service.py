from app.services.chunking_service import chunk_text
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore


class DocumentIndexService:
    def __init__(self, document_service: DocumentService | None = None):
        self.document_service = document_service or DocumentService()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore(dim=1536)
        self._indexed_document_ids: set[str] = set()

    def index_document(self, document_id: str, text: str) -> None:
        if document_id in self._indexed_document_ids:
            return

        chunks = chunk_text(text)

        for chunk in chunks:
            embedding = self.embedding_service.embed(chunk)
            self.vector_store.add(embedding, chunk)

        self._indexed_document_ids.add(document_id)

    def index_all_documents(self) -> int:
        indexed_count = 0

        for document in self.document_service.list_documents():
            document_id = document["id"]

            if document_id in self._indexed_document_ids:
                continue

            full_document = self.document_service.read_document(document_id)
            self.index_document(document_id, full_document["content"])
            indexed_count += 1

        return indexed_count

    def query(self, query: str, k: int = 3) -> list[str]:
        self.index_all_documents()
        embedding = self.embedding_service.embed(query)
        return self.vector_store.search(embedding, k=k)
