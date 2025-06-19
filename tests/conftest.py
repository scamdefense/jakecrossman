import sys
import os
import pytest
from app import create_app
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app("testing")
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()
