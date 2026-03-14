"""
run_cmd.py — Generic command runner adapter with scope/timeout enforcement.

Used by bbctl.py and can be invoked standalone for ad-hoc commands.

Usage:
    python tools/adapters/run_cmd.py <command> [args...]
"""
import json
import shlex
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def load_scope() -> dict:
    """Load the locked scope configuration."""
    scope_path = REPO / "scope" / "scope_lock.json"
    return json.loads(scope_path.read_text(encoding="utf-8"))


def run(cmd: list[str], cwd: Path = REPO, timeout_s: int = 300) -> dict:
    """
    Execute a command with timeout enforcement.
    Returns a dict with rc, stdout, stderr, and duration.
    """
    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        duration = time.time() - start
        return {
            "rc": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration_s": round(duration, 2),  # type: ignore[call-overload]
            "timed_out": False,
        }
    except subprocess.TimeoutExpired:
        duration = time.time() - start
        return {
            "rc": -1,
            "stdout": "",
            "stderr": f"Command timed out after {timeout_s}s",
            "duration_s": round(duration, 2),  # type: ignore[call-overload]
            "timed_out": True,
        }
    except FileNotFoundError:
        return {
            "rc": -1,
            "stdout": "",
            "stderr": f"Tool not found: {cmd[0]}",  # type: ignore[index]
            "duration_s": 0,
            "timed_out": False,
        }


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python run_cmd.py <command> [args...]")
        sys.exit(1)

    cmd = sys.argv[1:]  # type: ignore[index]
    scope = load_scope()
    timeout = int(
        scope.get("rate_limits", {})
        .get("tool_timeouts_seconds", {})
        .get("default", 300)
    )

    print(f"Running: {shlex.join(cmd)} (timeout={timeout}s)")
    result = run(cmd, timeout_s=timeout)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
