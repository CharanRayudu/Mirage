import os
import pytest

REQUIRED_FILES = [
    "Dockerfile",
    "docker-compose.yml",
    "requirements.txt",
    ".gitignore",
    ".env.example",
    "mirage/main.py",
]

def test_required_files_exist():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    for filename in REQUIRED_FILES:
        filepath = os.path.join(base_dir, filename)
        assert os.path.exists(filepath), f"Missing required file: {filename}"

def test_no_hardcoded_secrets():
    """Simple check to ensure no obvious hardcoded secrets like 'sk-...' are in python files."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    
    for root, _, files in os.walk(base_dir):
        if "venv" in root or ".git" in root or "__pycache__" in root:
            continue
            
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Very basic check for OpenAI-style keys, can be expanded
                    secret_prefix = "sk-" + "proj-"
                    assert secret_prefix not in content, f"Potential hardcoded secret found in {file}"
