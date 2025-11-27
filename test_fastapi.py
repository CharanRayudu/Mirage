import urllib.request
import traceback

print("Testing FastAPI import with patch...")
try:
    import fastapi
    print("FastAPI imported successfully")
except Exception:
    traceback.print_exc()
