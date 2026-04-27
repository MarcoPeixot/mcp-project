import argparse
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.tools.document_tools import register_document_tools

mcp = FastMCP("document-mcp-server")

register_document_tools(mcp)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the document MCP server.")
    parser.add_argument(
        "--transport",
        choices=("auto", "stdio", "streamable-http", "sse"),
        default="auto",
        help="Transport to run. 'auto' uses HTTP for interactive terminals and stdio otherwise.",
    )
    parser.add_argument(
        "--host",
        default=None,
        help="Host interface for HTTP transports. Defaults to the FastMCP setting.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port for HTTP transports. Defaults to the FastMCP setting.",
    )
    return parser.parse_args()


def _resolve_transport(transport: str) -> str:
    if transport != "auto":
        return transport

    if sys.stdin.isatty() and sys.stdout.isatty():
        print(
            "Interactive terminal detected; starting Streamable HTTP on "
            f"http://{mcp.settings.host}:{mcp.settings.port}{mcp.settings.streamable_http_path}. "
            "Use --transport stdio when launching from an MCP client.",
            file=sys.stderr,
        )
        return "streamable-http"

    return "stdio"


def _apply_runtime_settings(args: argparse.Namespace) -> None:
    if args.host is not None:
        mcp.settings.host = args.host

    if args.port is not None:
        mcp.settings.port = args.port


if __name__ == "__main__":
    args = _parse_args()
    _apply_runtime_settings(args)
    mcp.run(_resolve_transport(args.transport))
