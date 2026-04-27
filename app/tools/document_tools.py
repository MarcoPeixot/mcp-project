from typing import Any
from mcp.server.fastmcp import FastMCP
from app.services.document_service import DocumentService

document_service = DocumentService()

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
            "metadata": document["metadata"]
        }