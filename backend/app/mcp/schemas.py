from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ToolInputSchema(BaseModel):
    type: str = "object"
    properties: Dict[str, Any]
    required: List[str] = []

class ToolDefinition(BaseModel):
    name: str
    description: str
    input_schema: ToolInputSchema

class ToolListResponse(BaseModel):
    tools: List[ToolDefinition]

class ToolCallRequest(BaseModel):
    name: str
    arguments: Dict[str, Any]

class ToolCallResponse(BaseModel):
    content: List[Dict[str, Any]]
