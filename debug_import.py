import sys
import os
import traceback

print(f"Python version: {sys.version}")

print("\n--- Testing requests ---")
try:
    import requests
    print("requests imported successfully")
except Exception:
    traceback.print_exc()

print("\n--- Testing fastapi ---")
try:
    import fastapi
    print("fastapi imported successfully")
except Exception:
    traceback.print_exc()

print("\n--- Testing app import ---")
try:
    sys.path.append(os.path.join(os.getcwd(), "backend"))
    from app.main import app
    print("app imported successfully")
except Exception:
    traceback.print_exc()
