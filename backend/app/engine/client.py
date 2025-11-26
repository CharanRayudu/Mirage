from openai import OpenAI
from app.core.config import settings
from app.engine.prompts import SYSTEM_PROMPTS

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=settings.NVIDIA_API_KEY
)

def generate_hallucination(context: str, type: str = "default") -> str:
    """
    Generate fake content using Nvidia Nemotron.
    """
    system_prompt = SYSTEM_PROMPTS.get(type, SYSTEM_PROMPTS["default"])
    
    try:
        completion = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context}
            ],
            temperature=0.7,
            top_p=1,
            max_tokens=1024,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating hallucination: {e}")
        return f"[Error generating content: {str(e)}]"
