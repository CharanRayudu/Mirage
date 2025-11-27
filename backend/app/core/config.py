import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "MIRAGE"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Security & Secrets
    NVIDIA_API_KEY: str = os.getenv("NVIDIA_API_KEY", "")
    MCP_SERVER_PORT: int = int(os.getenv("MCP_SERVER_PORT", "8000"))
    LLM_MODEL: str = os.getenv("LLM_MODEL", "nvidia/nvidia-nemotron-nano-9b-v2")

settings = Settings()
