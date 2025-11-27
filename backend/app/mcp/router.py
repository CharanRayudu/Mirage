from app.mcp.schemas import ToolListResponse, ToolCallRequest, ToolCallResponse
from app.mcp.registry import registry
import json

# Logic functions decoupled from FastAPI

def list_tools_logic():
    return ToolListResponse(tools=registry.get_tools()).model_dump()

def call_tool_logic(request_data: dict):
    try:
        request = ToolCallRequest(**request_data)
        from app.core.logger import logger
        logger.log(f"Tool Call Requested: {request.name} with args {request.arguments}")
        
        tool_func = registry.get_tool(request.name)
        if not tool_func:
            logger.log(f"Tool {request.name} not found", "ERROR")
            return {"error": f"Tool {request.name} not found", "code": 404}
        
        result = tool_func(**request.arguments)
        logger.log(f"Tool {request.name} executed successfully")
        
        response = ToolCallResponse(content=[{"type": "text", "text": str(result)}])
        return response.model_dump()
    except Exception as e:
        from app.core.logger import logger
        logger.log(f"Error executing tool: {str(e)}", "ERROR")
        return {"error": str(e), "code": 500}
