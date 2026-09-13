# MCP Server
# Exposes agent tools over the Model Context Protocol

from mcp.server import FastMCP

mcp = FastMCP("AI Production Incident Resolution Agent")


@mcp.tool()
def resolve_incident(incident: str) -> str:
    """Run the full incident resolution pipeline for the given incident description."""
    from app.graph.graph import run_graph
    result = run_graph(incident)
    return result
