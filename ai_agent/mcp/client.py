# MCP Client
# Client utilities to interact with the MCP server

import asyncio
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters


async def call_resolve_incident(incident: str) -> str:
    """Send an incident to the MCP server and return the resolution."""
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp.server"],
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("resolve_incident", {"incident": incident})
            return result.content[0].text


if __name__ == "__main__":
    import sys
    incident = " ".join(sys.argv[1:]) or "Payment service is returning 500 errors."
    print(asyncio.run(call_resolve_incident(incident)))
