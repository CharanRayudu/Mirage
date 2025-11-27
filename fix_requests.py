import sys
import traceback

print("Attempting fix...")
try:
    import urllib.request
    import requests
    print("Imported requests successfully after fix")
except Exception:
    traceback.print_exc()
