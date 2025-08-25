from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
from .config import settings
from typing import Optional
from pydantic import SecretStr

class AgentManager:
    _client: Optional[MCPClient] = None
    _agent: Optional[MCPAgent] = None

    @classmethod
    def get_agent(cls):
        if cls._agent is None:
            cls._client = MCPClient.from_config_file(settings.mcp_config_file)
            llm = ChatGroq(
                model=settings.model_name,
                api_key=SecretStr(settings.groq_api_key)
            )
            cls._agent = MCPAgent(
                llm=llm,
                client=cls._client,
                max_steps=settings.max_steps,
                memory_enabled=True
            )
        return cls._agent

    @classmethod
    async def shutdown(cls):
        if cls._client and cls._client.sessions:
            await cls._client.close_all_sessions()
