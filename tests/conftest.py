import pytest
from app import create_app


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
