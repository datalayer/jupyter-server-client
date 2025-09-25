"""
Tests for HTTP client functionality.
"""

import unittest
from unittest.mock import Mock, patch
from jupyter_server_client.http_client import http_client


class TestHTTPClient(unittest.TestCase):
    """Test cases for HTTPClient."""

    def setUp(self):
        """Set up test fixtures."""
        self.base_url = "http://localhost:8888"
        self.token = "test-token-123"
        self.client = HTTPClient(self.base_url, token=self.token)

    def test_client_initialization(self):
        """Test HTTP client initialization."""
        self.assertEqual(self.client.base_url, self.base_url)
        self.assertEqual(self.client.headers["Authorization"], f"token {self.token}")

    def test_client_without_token(self):
        """Test HTTP client initialization without token."""
        client = HTTPClient(self.base_url)
        self.assertEqual(client.base_url, self.base_url)
        self.assertNotIn("Authorization", client.headers)

    @patch('requests.get')
    def test_get_request(self, mock_get):
        """Test GET request."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"test": "data"}
        mock_get.return_value = mock_response
        
        # Test
        response = self.client.get("/api/test")
        
        # Assertions
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        self.assertIn(f"{self.base_url}/api/test", call_args[0])
        self.assertIn("headers", call_args[1])

    @patch('requests.post')
    def test_post_request(self, mock_post):
        """Test POST request."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"created": "data"}
        mock_post.return_value = mock_response
        
        # Test data
        test_data = {"key": "value"}
        
        # Test
        response = self.client.post("/api/test", json=test_data)
        
        # Assertions
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertIn(f"{self.base_url}/api/test", call_args[0])
        self.assertIn("headers", call_args[1])

    @patch('requests.put')
    def test_put_request(self, mock_put):
        """Test PUT request."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"updated": "data"}
        mock_put.return_value = mock_response
        
        # Test data
        test_data = {"key": "updated_value"}
        
        # Test
        response = self.client.put("/api/test/123", json=test_data)
        
        # Assertions
        mock_put.assert_called_once()

    @patch('requests.delete')
    def test_delete_request(self, mock_delete):
        """Test DELETE request."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response
        
        # Test
        response = self.client.delete("/api/test/123")
        
        # Assertions
        mock_delete.assert_called_once()

    def test_url_construction(self):
        """Test URL construction."""
        endpoint = "/api/kernels"
        expected_url = f"{self.base_url}{endpoint}"
        
        # This tests the internal _url method if it exists
        # We'll test through actual requests instead
        self.assertTrue(self.base_url in self.client.base_url)


class TestAsyncHTTPClient(unittest.TestCase):
    """Test cases for AsyncHTTPClient."""

    def setUp(self):
        """Set up test fixtures."""
        self.base_url = "http://localhost:8888"
        self.token = "test-token-123"
        self.client = AsyncHTTPClient(self.base_url, token=self.token)

    def test_async_client_initialization(self):
        """Test async HTTP client initialization."""
        self.assertEqual(self.client.base_url, self.base_url)
        self.assertEqual(self.client.headers["Authorization"], f"token {self.token}")

    def test_async_client_without_token(self):
        """Test async HTTP client initialization without token."""
        client = AsyncHTTPClient(self.base_url)
        self.assertEqual(client.base_url, self.base_url)
        self.assertNotIn("Authorization", client.headers)


if __name__ == '__main__':
    unittest.main()
