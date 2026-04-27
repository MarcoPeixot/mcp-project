import os
from typing import Any

from openai import OpenAI
from mcp.server.fastmcp import FastMCP

from app.services.document_service import DocumentService
from app.services.index_service import DocumentIndexService

document_service = DocumentService()
index_service: DocumentIndexService | None = None


def _get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required for this tool.")

    return OpenAI(api_key=api_key)


def _get_index_service() -> DocumentIndexService:
    global index_service

    if index_service is None:
        index_service = DocumentIndexService(document_service=document_service)

    return index_service


def register_document_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    def list_documents() -> list[dict[str, Any]]:
        """
        List all available documents.
        """
        return document_service.list_documents()

    @mcp.tool()
    def read_document(document_id: str) -> dict[str, Any]:
        """
        Read the full content of a document by its ID.
        """
        return document_service.read_document(document_id)

    @mcp.tool()
    def search_document(query: str) -> list[dict[str, Any]]:
        """
        Search documents by a text query.
        """
        return document_service.search_document(query)

    @mcp.tool()
    def get_document_metadata(document_id: str) -> dict[str, Any]:
        """
        Get metadata for a specific document.
        """
        document = document_service.read_document(document_id)

        return {
            "id": document["id"],
            "title": document["title"],
            "metadata": document["metadata"],
        }

    @mcp.tool()
    def semantic_search(query: str, k: int = 3) -> list[str]:
        """
        Search documents using semantic similarity.
        """
        return _get_index_service().query(query, k=k)

    @mcp.tool()
    def answer_question(query: str, k: int = 3) -> dict[str, Any]:
        """
        Answer a question based on documents using semantic retrieval.
        """
        chunks = _get_index_service().query(query, k=k)
        if not chunks:
            return {
                "answer": "No relevant document chunks were found.",
                "sources": [],
            }

        context = "\n\n".join(chunks)
        client = _get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Answer based only on the provided context.",
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {query}",
                },
            ],
        )

        return {
            "answer": response.choices[0].message.content,
            "sources": chunks,
        }
