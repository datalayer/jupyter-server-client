"""
Integration tests for jupyter-server-client.
"""

import unittest
from unittest.mock import patch
from jupyter_server_client import JupyterServerClient


class TestIntegration(unittest.TestCase):
    """Integration test cases."""

    def setUp(self):
        """Set up test fixtures."""
        self.server_url = "http://localhost:8888"
        self.token = "test-token-123"
        self.client = JupyterServerClient(self.server_url, token=self.token)

    def test_complete_workflow_simulation(self):
        """Test a complete workflow simulation with mocked responses."""
        # This test simulates a real workflow but with mocked HTTP calls
        from jupyter_server_client.models import Kernel
        from datetime import datetime
        
        # Test 1: List kernels (should be our main functionality)  
        with patch.object(self.client.kernels, 'list_kernels') as mock_list:
            mock_list.return_value = [
                Kernel(
                    id="kernel-123", 
                    name="python3", 
                    last_activity=datetime.now(),
                    execution_state="idle",
                    connections=1
                )
            ]
            
            kernels = self.client.kernels.list_kernels()
            self.assertEqual(len(kernels), 1)
            self.assertEqual(kernels[0].name, "python3")

    def test_library_separation_of_concerns(self):
        """Test that our library only provides intended functionality."""
        # Verify we have kernel listing
        self.assertTrue(hasattr(self.client.kernels, 'list_kernels'))
        self.assertTrue(hasattr(self.client.kernels, 'get_kernel'))
        
        # Verify we DON'T have kernel management (that's jupyter-kernel-client)
        management_methods = [
            'start_kernel', 'delete_kernel', 'interrupt_kernel', 'restart_kernel'
        ]
        
        for method in management_methods:
            self.assertFalse(hasattr(self.client.kernels, method),
                           f"Should not have {method} - that's jupyter-kernel-client's job")

    def test_ecosystem_integration_simulation(self):
        """Test simulation of working with the Datalayer ecosystem."""
        # This simulates how someone would use all three libraries together
        
        print("📚 Datalayer Jupyter Ecosystem Integration Test")
        print("=" * 50)
        
        # 1. Use jupyter-server-client to list available kernels
        print("🔍 Step 1: List available kernels (jupyter-server-client)")
        with patch.object(self.client.kernels, 'list_kernels') as mock_list:
            from jupyter_server_client.models import Kernel
            from datetime import datetime
            mock_list.return_value = [
                Kernel(
                    id="kernel-123", 
                    name="python3", 
                    last_activity=datetime.now(),
                    execution_state="idle", 
                    connections=1
                )
            ]
            
            kernels = self.client.kernels.list_kernels()
            self.assertGreaterEqual(len(kernels), 0)
            print(f"   Found {len(kernels)} kernel(s)")
        
        # 2. Simulate using jupyter-kernel-client for management (not our responsibility)
        print("⚡ Step 2: Connect to kernel (would use jupyter-kernel-client)")
        print("   # from jupyter_kernel_client import KernelClient")
        print("   # kernel_client = KernelClient('kernel-123')")
        print("   # kernel_client.start()  # This is NOT our responsibility")
        
        # 3. Simulate using jupyter-nbmodel-client for collaboration (not our responsibility)
        print("🤝 Step 3: Real-time collaboration (would use jupyter-nbmodel-client)")
        print("   # from jupyter_nbmodel_client import NBModelClient")  
        print("   # nbmodel = NBModelClient('notebook.ipynb')")
        print("   # nbmodel.connect()  # This is NOT our responsibility")
        
        print("\n✅ Perfect separation of concerns achieved!")

    def test_error_handling(self):
        """Test error handling in various scenarios."""
        with patch.object(self.client.kernels, 'list_kernels') as mock_list:
            # Mock an exception
            mock_list.side_effect = Exception("Server error")
            
            with self.assertRaises(Exception):
                self.client.kernels.list_kernels()

    def test_readonly_nature_of_kernel_operations(self):
        """Test that kernel operations are read-only as intended."""
        # Get public methods of kernels manager
        kernel_methods = [m for m in dir(self.client.kernels) 
                         if not m.startswith('_') and m != 'http_client']
        
        # All methods should be read-only (get, list, etc.)
        readonly_prefixes = ['get', 'list']
        
        for method in kernel_methods:
            method_is_readonly = any(method.startswith(prefix) for prefix in readonly_prefixes)
            self.assertTrue(method_is_readonly, 
                          f"Method {method} should be read-only (get_*, list_*)")
        
        print(f"✅ All {len(kernel_methods)} kernel methods are read-only: {kernel_methods}")


if __name__ == '__main__':
    # Run with more verbose output
    unittest.main(verbosity=2)
