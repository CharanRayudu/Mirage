from app.mcp.schemas import ToolListResponse, ToolCallRequest, ToolCallResponse
from app.mcp.registry import registry
import json

# Logic functions decoupled from FastAPI

def list_tools_logic():
    return ToolListResponse(tools=registry.get_tools()).model_dump()

def call_tool_logic(request_data: dict):
    try:
        request = ToolCallRequest(**request_data)
        tool_func = registry.get_tool(request.name)
        if not tool_func:
            return {"error": f"Tool {request.name} not found", "code": 404}
        
        result = tool_func(**request.arguments)
        response = ToolCallResponse(content=[{"type": "text", "text": str(result)}])
        return response.model_dump()
    except Exception as e:
        return {"error": str(e), "code": 500}
