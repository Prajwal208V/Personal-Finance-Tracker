# main.py  – single-file FastAPI app with “context-only” support
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, SecretStr
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY missing")

# ---------- one-time agent init ----------
MCP_CONFIG = "browser_mcp.json"
MODEL_NAME  = "gemma2-9b-it"
MAX_STEPS   = 15

client = MCPClient.from_config_file(MCP_CONFIG)
llm    = ChatGroq(model=MODEL_NAME, api_key=SecretStr(GROQ_API_KEY))
agent  = MCPAgent(llm=llm, client=client,
                  max_steps=MAX_STEPS, memory_enabled=True)

# ---------- FastAPI ----------
app = FastAPI(title="MCP Chat API")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    mode: str = Query("answer", enum=["answer", "context"])  # ← new switch
):
    try:
        # clear conversation if requested
        if payload.message.lower() == "clear":
            agent.clear_conversation_history()
            return ChatResponse(response="Conversation history cleared.")

        # ───────────────────────────────────────────────────────────────
        if mode == "context":
            observations = []
            async for item in agent.stream(payload.message):
                if not isinstance(item, str):
                    _action, observation = item
                    observations.append(str(observation))
            # return concatenated (or JSON, up to you)
            return ChatResponse(response="\n".join(observations))

        # default = full answer
        result = await agent.run(payload.message)
        return ChatResponse(response=result)
        # ───────────────────────────────────────────────────────────────

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
async def shutdown():
    if client and client.sessions:
        await client.close_all_sessions()
