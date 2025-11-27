import urllib.request
import traceback

print("Testing OpenAI import...")
try:
    import openai
    print("OpenAI imported successfully")
except Exception:
    traceback.print_exc()
