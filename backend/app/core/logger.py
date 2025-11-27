from collections import deque
from datetime import datetime

class InMemoryLogger:
    def __init__(self, max_len=100):
        self.logs = deque(maxlen=max_len)

    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}"
        self.logs.appendleft(entry)  # Newest first
        print(entry) # Also print to stdout for Docker logs

    def get_logs(self):
        return list(self.logs)

logger = InMemoryLogger()
