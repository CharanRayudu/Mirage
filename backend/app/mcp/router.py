from fastapi import APIRouter, HTTPException
from app.mcp.schemas import ToolListResponse, ToolCallRequest, ToolCallResponse
from app.mcp.registry import registry

router = APIRouter()

@router.get("/tools", response_model=ToolListResponse)
async def list_tools():
    """
    List available tools.
    """
    return ToolListResponse(tools=registry.get_tools())

@router.post("/tools/call", response_model=ToolCallResponse)
async def call_tool(request: ToolCallRequest):
    """
    Call a tool.
    """
    tool_func = registry.get_tool(request.name)
    if not tool_func:
        raise HTTPException(status_code=404, detail=f"Tool {request.name} not found")
    
    try:
        result = tool_func(**request.arguments)
        return ToolCallResponse(content=[{"type": "text", "text": str(result)}])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
