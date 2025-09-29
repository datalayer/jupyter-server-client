"""
Test configuration and fixtures for jupyter-server-api tests.
"""

import pytest
from unittest.mock import Mock, AsyncMock
from jupyter_server_api import JupyterServerClient


@pytest.fixture
def mock_server_url():
    """Mock Jupyter server URL."""
    return "http://localhost:8888"


@pytest.fixture
def mock_token():
    """Mock authentication token."""
    return "test-token-123"


@pytest.fixture
def client(mock_server_url, mock_token):
    """Create a JupyterServerClient instance for testing."""
    return JupyterServerClient(mock_server_url, token=mock_token)


@pytest.fixture
def mock_response():
    """Mock HTTP response."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {}
    return response


@pytest.fixture
def mock_async_response():
    """Mock async HTTP response."""
    response = AsyncMock()
    response.status = 200
    response.json.return_value = {}
    return response


@pytest.fixture
def sample_kernel_data():
    """Sample kernel data for testing."""
    return {
        "id": "test-kernel-123",
        "name": "python3",
        "last_activity": "2023-12-01T10:00:00Z",
        "execution_state": "idle",
        "connections": 1
    }


@pytest.fixture
def sample_kernels_list(sample_kernel_data):
    """Sample list of kernels for testing."""
    return [
        sample_kernel_data,
        {
            "id": "test-kernel-456",
            "name": "python3",
            "last_activity": "2023-12-01T09:30:00Z",
            "execution_state": "busy",
            "connections": 2
        }
    ]


@pytest.fixture
def sample_content_data():
    """Sample content data for testing."""
    return {
        "name": "test.ipynb",
        "path": "notebooks/test.ipynb",
        "type": "notebook",
        "writable": True,
        "last_modified": "2023-12-01T10:00:00Z",
        "created": "2023-12-01T09:00:00Z",
        "content": None,
        "format": None,
        "mimetype": None,
        "size": 1024
    }


@pytest.fixture
def sample_session_data():
    """Sample session data for testing."""
    return {
        "id": "session-123",
        "path": "notebooks/test.ipynb",
        "name": "",
        "type": "notebook",
        "kernel": {
            "id": "kernel-456",
            "name": "python3"
        }
    }
