from threading import Lock
from typing import Dict


class Metrics:
    def __init__(self):
        self._lock = Lock()
        self._counters: Dict[str, int] = {
            "tool_calls_total": 0,
            "tool_errors_total": 0,
            "requests_total": 0,
        }

    def inc(self, key: str, value: int = 1):
        with self._lock:
            self._counters[key] = self._counters.get(key, 0) + value

    def snapshot(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._counters)


metrics = Metrics()
