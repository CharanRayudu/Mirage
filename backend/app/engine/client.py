from app.core.config import settings
from app.engine.prompts import SYSTEM_PROMPTS
import random

# Mock client - no OpenAI import
client = None

def generate_hallucination(context: str, type: str = "default") -> str:
    """
    Generate fake content using a mock implementation (since OpenAI lib is broken on Py3.14).
    """
    system_prompt = SYSTEM_PROMPTS.get(type, SYSTEM_PROMPTS["default"])
    
    # Simple deterministic mock response
    responses = [
        f"This is a hallucination based on '{context}'. System says: {system_prompt[:20]}...",
        "Access Denied. Security Protocol 7 engaged.",
        "Error: Log file corrupted. Please contact admin.",
        "CONFIDENTIAL: Project Mirage blueprint found."
    ]
    
    return random.choice(responses)
