# Create server parameters for stdio connection
from mcp import ClientSession
from mcp.client.sse import sse_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
import asyncio


model = ChatOllama(model="gpt-oss:20b")
proxy_url = "http://127.0.0.1:8081/sse"

async def run_agent():
    async with sse_client(proxy_url) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # Load MCP tools into LangChain format
            tools = await load_mcp_tools(session)
            # Create and run the agent
            agent = create_react_agent(model, tools)
            query = input("Inserisci la tua richiesta: ")
            agent_response = await agent.ainvoke({"messages": query})
            return agent_response

async def main():
    while True:
        result = await run_agent()
        rispostaTool = None
        rispostaAI = None

        for msg in result["messages"]:
            if msg.__class__.__name__ == "ToolMessage":
                rispostaTool = msg
                
            elif msg.__class__.__name__ == "AIMessage":
                rispostaAI = msg

        if rispostaTool is None:
            print("Risposta: ", rispostaAI.content)
        else:
            print("Tool utilizzato: ", rispostaTool.name, ", Messaggio del tool: ", rispostaTool.content, "Messaggio dell'agente: ", rispostaAI.content)

if __name__ == "__main__":
    asyncio.run(main())