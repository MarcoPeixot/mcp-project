# Document MCP Server

Small MCP server that exposes local text documents as tools.

## Run It

For normal manual development, run the server as a Python module:

```bash
uv run python -m app.main
```

When launched from an interactive terminal, the server defaults to `streamable-http`
at `http://127.0.0.1:8000/mcp` so it does not try to parse terminal input as JSON-RPC.

To force MCP stdio mode for a real MCP client:

```bash
uv run python -m app.main --transport stdio
```

Useful environment variables:

```bash
FASTMCP_HOST=127.0.0.1
FASTMCP_PORT=8000
FASTMCP_LOG_LEVEL=DEBUG
```

You can also override host and port directly from the CLI:

```bash
uv run python -m app.main --port 8001
uv run python -m app.main --host 0.0.0.0 --port 8001
```
