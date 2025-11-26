from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.get("/")
def root():
    return {"message": "Welcome to MIRAGE"}

from app.mcp.router import router as mcp_router
app.include_router(mcp_router, prefix="/mcp", tags=["mcp"])
