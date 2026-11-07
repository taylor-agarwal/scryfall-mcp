from pathlib import Path

from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI
from langchain.mcp import MCPAdapter

server_path = Path(__file__).parent.parent / "src" / "scryfall_mcp" / "server.py"
mcp_config = {
    "scryfall": {
        "command": "python",
        "args": [str(server_path)]
    }
}

async def main(query: str):
    # model = ChatOpenAI(model="gpt-5.6-luna")
    model = "ollama:gemma4:e2b"
    
    async with MCPAdapter(mcp_config) as adapter:
        tools = await adapter.list_tools()
        agent = create_deep_agent(
            model=model,
            tools=tools,
        )
        response = await agent.ainvoke(input={"messages": [{"role": "user", "content": query}]})
    
    return response
        
if __name__ == "__main__":
    import asyncio
    
    query = "What is the current price for Savannah from the Alpha set?"
    response = asyncio.run(main(query))
    print(response)
