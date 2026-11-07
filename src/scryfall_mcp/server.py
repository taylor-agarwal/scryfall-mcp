import logging

from fastmcp import FastMCP

from scryfall_mcp.tools import get_cards, search

logger = logging.getLogger(__name__)


def build_server():
    """Build the MCP server."""
    # Create the server
    server = FastMCP(
        name="Scryfall",
        instructions="Provides tools for searching and fetching details about Magic: The Gathering cards.",
    )

    # Register tools
    tools = [
        get_cards,
        search,
    ]
    for tool in tools:
        server.add_tool(tool)

    return server


def main():
    """Run main process."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    server = build_server()
    server.run()

if __name__ == "__main__":
    main()
