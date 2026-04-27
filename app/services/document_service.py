from pathlib import Path
from typing import Any

DOCUMENTS_DIR = Path(__file__).resolve().parent.parent / "data" / "documents"
ALLOWED_EXTENSIONS = {".txt", ".md"}

class DocumentService:
    def __init__(self) -> None:
        DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

    def list_documents(self) -> list[dict[str, Any]]:
        documents = []
        for file in DOCUMENTS_DIR.iterdir():
            if file.is_file() and file.suffix in ALLOWED_EXTENSIONS:
                documents.append({
                    "id": file.name,
                    "title": file.stem.replace("_", " ").title(),
                    "filename": file.name,
                    "extension": file.suffix,
                    "size_bytes": file.stat().st_size,
                })
        return documents

    def read_document(self, document_id: str) -> dict[str, Any]:
        file_path = self._resolve_document_path(document_id)

        content = file_path.read_text(encoding="utf-8")

        return {
            "id": file_path.name,
            "title": file_path.stem.replace("_", " ").title(),
            "content": content,
            "metadata": {
                "extension": file_path.suffix,
                "size_bytes": file_path.stat().st_size,
            },
        }

    def _resolve_document_path(self, document_id: str) -> Path:
        normalized_document_id = document_id.strip()

        if not normalized_document_id:
            raise ValueError("document_id must not be empty.")

        file_path = (DOCUMENTS_DIR / normalized_document_id).resolve()

        if DOCUMENTS_DIR.resolve() not in file_path.parents:
            raise ValueError("document_id must point to a file inside the documents directory.")

        if not file_path.exists():
            raise FileNotFoundError(f"Document not found: {normalized_document_id}")

        if not file_path.is_file():
            raise IsADirectoryError(f"document_id must point to a file: {normalized_document_id}")

        if file_path.suffix not in ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Unsupported document extension '{file_path.suffix}'. Allowed: {sorted(ALLOWED_EXTENSIONS)}"
            )

        return file_path

    def search_document(self, query: str) -> list[dict[str, Any]]:
        query_lower = query.lower()
        results = []

        for document in self.list_documents():
            full_document = self.read_document(document["id"])
            content = full_document["content"]

            if query_lower in content.lower():
                index = content.lower().find(query_lower)
                start = max(index - 120, 0)
                end = min(index + 180, len(content))

                results.append({
                    "id": document["id"],
                    "title": document["title"],
                    "snippet": content[start:end]
                })

        return results
