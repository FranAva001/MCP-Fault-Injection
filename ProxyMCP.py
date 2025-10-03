from fastmcp import FastMCP, Context
from fastmcp.server.proxy import ProxyClient
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.exceptions import ToolError
import asyncio
import random
import json

class Unreachable(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        print("Esecuzione scenario Unreachable")

        tool_name = context.message.name
        
        #Rende irraggiungibile il tool
        raise ToolError(f"Accesso negato al tool:", tool_name)

class SlowResponse(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):

        print("Esecuzione scenario Slow Response")

        #Aspetta 5 minuti prima di restituire la risposta
        await asyncio.sleep(300)
        return await call_next(context)

class NonResponsive(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):

        print("Esecuzione scenario Non Responsive")
        pass

class IncorrectResponse(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):

        print("Esecuzione scenario Incorrect Response")

        result = await call_next(context)

        content = result.content[0].text
        words = json.loads(content)

        print(words)

        if not isinstance(words, str):
            delta_words = words + 0.3
        else:
            delta_words = []
            for word in words:
                if random.random() < 0.9:  # 90% probabilità di perturbare la parola
                    delta_word = "".join(reversed(word)) + "*"
                else:
                    delta_word = word
                delta_words.append(delta_word)

        result.content[0].text = str(delta_words)
        print(result.content)
        return result

proxy_client = ProxyClient("http://127.0.0.1:8000/sse")

# Proxy che espone le capacità del client
proxy = FastMCP.as_proxy(proxy_client, name="SQLite Proxy")
proxy.add_middleware(IncorrectResponse())

    
@proxy.tool("greetings")
async def greetings(content: str, ctx: Context) -> str:
    await ctx.info("Ciao")
    return "Funziona"

async def main():
    await proxy.run_async(transport="sse", host="127.0.0.1", port=8081)

if __name__ == "__main__":
    asyncio.run(main()) 