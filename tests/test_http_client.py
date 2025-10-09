"""
Tests for HTTP client functionality.
"""

import unittest
from unittest.mock import Mock, patch
from jupyter_server_api.http_client import BaseHTTPClient


class TestHTTPClient(unittest.TestCase):
    """Test cases for BaseHTTPClient."""

    def setUp(self):
        """Set up test fixtures."""
        self.base_url = "http://localhost:8888"
        self.token = "test-token-123"
        self.client = BaseHTTPClient(self.base_url, token=self.token)

    def test_client_initialization(self):
        """Test HTTP client initialization."""
        # Base URL should end with / after initialization
        self.assertEqual(self.client.base_url, "http://localhost:8888/")
        self.assertIn("Authorization", self.client.session.headers)
        self.assertEqual(self.client.session.headers["Authorization"], f"Bearer {self.token}")

    def test_client_without_token(self):
        """Test HTTP client initialization without token."""
        client = BaseHTTPClient(self.base_url)
        self.assertEqual(client.base_url, "http://localhost:8888/")
        self.assertNotIn("Authorization", client.session.headers)

    def test_base_url_normalization(self):
        """Test that base URL is normalized to end with /."""
        # Test with trailing slash
        client1 = BaseHTTPClient("http://localhost:8888/")
        self.assertEqual(client1.base_url, "http://localhost:8888/")
        
        # Test without trailing slash
        client2 = BaseHTTPClient("http://localhost:8888")
        self.assertEqual(client2.base_url, "http://localhost:8888/")
        
        # Test with multiple trailing slashes
        client3 = BaseHTTPClient("http://localhost:8888///")
        self.assertEqual(client3.base_url, "http://localhost:8888/")

    def test_url_construction_with_path_prefix(self):
        """Test URL construction when base_url contains path segments.
        
        This is the critical test for the bug fix - ensuring path prefixes
        are not lost when using urljoin.
        """
        # Test case from the bug report
        client = BaseHTTPClient("http://dsw-xxx:8890/dsw-xxx/")
        url = client._build_url("/api/contents/nb.ipynb")
        expected = "http://dsw-xxx:8890/dsw-xxx/api/contents/nb.ipynb"
        self.assertEqual(url, expected)
        
        # Test without trailing slash in input
        client2 = BaseHTTPClient("http://dsw-xxx:8890/dsw-xxx")
        url2 = client2._build_url("/api/contents/nb.ipynb")
        self.assertEqual(url2, expected)

    def test_url_construction_multiple_path_segments(self):
        """Test URL construction with multiple path segments in base_url."""
        client = BaseHTTPClient("http://host:8888/prefix/subpath/")
        url = client._build_url("/api/kernels")
        expected = "http://host:8888/prefix/subpath/api/kernels"
        self.assertEqual(url, expected)

    def test_url_construction_without_prefix(self):
        """Test URL construction with base_url at root (no path prefix)."""
        client = BaseHTTPClient("http://localhost:8888")
        url = client._build_url("/api/contents/test.ipynb")
        expected = "http://localhost:8888/api/contents/test.ipynb"
        self.assertEqual(url, expected)

    def test_url_construction_various_paths(self):
        """Test URL construction with various API paths."""
        client = BaseHTTPClient("http://host:8888/jupyter/")
        
        test_cases = [
            ("/api/kernels", "http://host:8888/jupyter/api/kernels"),
            ("/api/contents/", "http://host:8888/jupyter/api/contents/"),
            ("/api/sessions/123", "http://host:8888/jupyter/api/sessions/123"),
            ("api/status", "http://host:8888/jupyter/api/status"),  # Without leading slash
        ]
        
        for path, expected in test_cases:
            with self.subTest(path=path):
                url = client._build_url(path)
                self.assertEqual(url, expected)


if __name__ == '__main__':
    unittest.main()
