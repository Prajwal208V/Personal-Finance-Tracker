from pydantic import BaseSettings, Field

class Settings(
    # BaseSettings,
    ):
    groq_api_key: str = Field(..., alias="GROQ_API_KEY")
    mcp_config_file: str = "browser_mcp.json"
    model_name: str = "qwen-qwq-32b"
    max_steps: int = 15

    class Config:
        env_file = ".env"

settings = Settings()
