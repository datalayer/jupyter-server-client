"""
Tests for the main JupyterServerClient class.
"""

import unittest

from jupyter_server_client import JupyterServerClient


class TestJupyterServerClient(unittest.TestCase):
    """Test cases for JupyterServerClient."""

    def setUp(self):
        """Set up test fixtures."""
        self.server_url = "http://localhost:8888"
        self.token = "test-token-123"
        self.client = JupyterServerClient(self.server_url, token=self.token)

    def test_client_initialization(self):
        """Test client initialization."""
        # Test that managers are properly initialized
        self.assertIsNotNone(self.client.contents)
        self.assertIsNotNone(self.client.sessions)
        self.assertIsNotNone(self.client.terminals)
        self.assertIsNotNone(self.client.kernelspecs)
        self.assertIsNotNone(self.client.kernels)

    def test_client_managers_available(self):
        """Test that all expected managers are available."""
        expected_managers = ['contents', 'sessions', 'terminals', 'kernelspecs', 'kernels']
        
        for manager in expected_managers:
            with self.subTest(manager=manager):
                self.assertTrue(hasattr(self.client, manager))

    def test_client_with_custom_timeout(self):
        """Test client initialization with custom timeout."""
        timeout = 60
        client = JupyterServerClient(self.server_url, token=self.token, timeout=timeout)
        # Just test that it initializes without error
        self.assertIsNotNone(client)

    def test_client_without_token(self):
        """Test client initialization without token."""
        client = JupyterServerClient(self.server_url)
        # Just test that it initializes without error
        self.assertIsNotNone(client)

    def test_client_repr(self):
        """Test client string representation."""
        repr_str = repr(self.client)
        self.assertIn("JupyterServerClient", repr_str)


if __name__ == '__main__':
    unittest.main()
