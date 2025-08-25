import asyncio

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from mcp_use import MCPAgent, MCPClient, client
import os


async def run_memory_chat():
    # Run a chat using MCPAgent's built-in conversation memory
    # Load environment variables for API keys
    load_dotenv()
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key
    else:
        raise ValueError("GROQ_API_KEY is not set")
         
    config_file = "browser_mcp.json"
    client = MCPClient.from_config_file(config_file)
    llm = ChatGroq(model="qwen-qwq-32b")

    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True,
    )
    print("================")
    print("Starting chat...")
    print("================")

    try:
        while True:

            user_input = input("\nYou: ")

            if user_input.lower() in ["quit", "exit"]:
                print("Ending conversation...")
                break
            
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

           
            print(f"\n Assistant:",end="", flush=True)

            try:
                response = await agent.run(user_input)
                print(response)
                
            except Exception as e:
                print(f"Error: {e}")
                
    finally:
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())



'''  "playwright": {
        "command": "npx",
        "args": [
            "@playwright/mcp@latest"
        ]
      },
      "airbnb": {
          "command": "npx",
          "args": [
            "-y",
            "@openbnb/mcp-server-airbnb"
          ]
      },
      "duckduckgo-search": {
        "command": "npx",
        "args": [
          "-y",
          "duckduckgo-mcp-server"
        ]
      }, 
      
      "fi_mcp": {
        "command": "npx",
        "args": [
          "mcp-remote", 
          "https://mcp.fi.money:8080/mcp/stream"
        ]
      }
      
      '''