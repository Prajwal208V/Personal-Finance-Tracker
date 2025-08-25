from fastapi import FastAPI
from app.api.v1.chat import router as chat_router
from app.agent import AgentManager
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await AgentManager.shutdown()

def create_app():
    app = FastAPI(title="MCP Chat API", lifespan=lifespan)
    app.include_router(chat_router)
    return app

app = FastAPI()
