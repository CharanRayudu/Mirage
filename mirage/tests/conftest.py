import sys
import os
import pytest
# from fastapi.testclient import TestClient

# Add the parent directory to sys.path so we can import mirage.main
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from mirage.main import app
    return TestClient(app)
