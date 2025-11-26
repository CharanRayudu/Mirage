from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "MIRAGE"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Security & Secrets
    NVIDIA_API_KEY: str
    MCP_SERVER_PORT: int = 8000
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
