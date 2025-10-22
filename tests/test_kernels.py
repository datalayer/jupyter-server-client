"""
Tests for the KernelsManager class.
"""

import unittest
from unittest.mock import Mock
from jupyter_server_client.managers.kernels import KernelsManager
from jupyter_server_client.models import Kernel


class TestKernelsManager(unittest.TestCase):
    """Test cases for KernelsManager."""

    def setUp(self):
        """Set up test fixtures."""
        self.http_client = Mock()
        self.manager = KernelsManager(self.http_client)

    def test_list_kernels_success(self):
        """Test successful kernel listing."""
        # Mock the http_client.get method directly
        self.http_client.get.return_value = [
            {
                "id": "kernel-123",
                "name": "python3",
                "last_activity": "2023-12-01T10:00:00Z",
                "execution_state": "idle",
                "connections": 1
            },
            {
                "id": "kernel-456", 
                "name": "python3",
                "last_activity": "2023-12-01T09:30:00Z",
                "execution_state": "busy",
                "connections": 2
            }
        ]
        
        # Test
        kernels = self.manager.list_kernels()
        
        # Assertions
        self.assertEqual(len(kernels), 2)
        self.assertIsInstance(kernels[0], Kernel)
        self.assertEqual(kernels[0].id, "kernel-123")
        self.assertEqual(kernels[1].execution_state, "busy")

    def test_list_kernels_empty(self):
        """Test kernel listing when no kernels exist."""
        # Mock the http_client.get method directly
        self.http_client.get.return_value = []
        
        # Test
        kernels = self.manager.list_kernels()
        
        # Assertions
        self.assertEqual(len(kernels), 0)
        self.assertIsInstance(kernels, list)

    def test_get_kernel_success(self):
        """Test successful kernel retrieval."""
        kernel_id = "kernel-123"
        
        # Mock the http_client.get method directly
        self.http_client.get.return_value = {
            "id": kernel_id,
            "name": "python3",
            "last_activity": "2023-12-01T10:00:00Z",
            "execution_state": "idle",
            "connections": 1
        }
        
        # Test
        kernel = self.manager.get_kernel(kernel_id)
        
        # Assertions
        self.assertIsInstance(kernel, Kernel)
        self.assertEqual(kernel.id, kernel_id)
        self.assertEqual(kernel.name, "python3")
        self.assertEqual(kernel.execution_state, "idle")

    def test_get_kernel_not_found(self):
        """Test kernel retrieval when kernel doesn't exist."""
        kernel_id = "nonexistent-kernel"
        
        # Mock the http_client.get method to raise an exception
        self.http_client.get.side_effect = Exception("Kernel not found")
        
        # Test and assertions
        with self.assertRaises(Exception):
            self.manager.get_kernel(kernel_id)

    def test_manager_has_only_listing_methods(self):
        """Test that manager only has listing methods, no management."""
        # Get all public methods (not starting with _)
        public_methods = [method for method in dir(self.manager) 
                         if not method.startswith('_') and method != 'http_client']
        
        # Expected methods (only listing/reading, no management)
        expected_methods = ['get_kernel', 'list_kernels']
        
        self.assertEqual(set(public_methods), set(expected_methods))

    def test_manager_no_management_methods(self):
        """Test that manager doesn't have management methods."""
        # Methods that should NOT exist (these are in jupyter-kernel-client)
        forbidden_methods = [
            'start_kernel', 'delete_kernel', 'interrupt_kernel', 
            'restart_kernel', 'create_kernel'
        ]
        
        for method in forbidden_methods:
            with self.subTest(method=method):
                self.assertFalse(hasattr(self.manager, method),
                               f"Manager should not have {method} method")


if __name__ == '__main__':
    unittest.main()
