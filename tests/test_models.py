"""
Tests for data models.
"""

import unittest

from jupyter_server_api.models import Kernel


class TestModels(unittest.TestCase):
    """Test cases for Pydantic models."""

    def test_kernel_model_creation(self):
        """Test Kernel model creation with valid data."""
        data = {
            "id": "kernel-123",
            "name": "python3",
            "last_activity": "2023-12-01T10:00:00Z",
            "execution_state": "idle",
            "connections": 1
        }
        
        kernel = Kernel(**data)
        
        self.assertEqual(kernel.id, "kernel-123")
        self.assertEqual(kernel.name, "python3")
        self.assertEqual(kernel.execution_state, "idle")
        self.assertEqual(kernel.connections, 1)

    def test_kernel_model_complete_fields(self):
        """Test Kernel model with all required fields."""
        from datetime import datetime
        data = {
            "id": "kernel-123",
            "name": "python3",
            "last_activity": datetime.now(),
            "execution_state": "idle",
            "connections": 1
        }
        
        kernel = Kernel(**data)
        
        self.assertEqual(kernel.id, "kernel-123")
        self.assertEqual(kernel.name, "python3")
        self.assertEqual(kernel.execution_state, "idle")
        self.assertEqual(kernel.connections, 1)

    def test_kernel_model_dict_conversion(self):
        """Test Kernel model dict conversion."""
        from datetime import datetime
        now = datetime.now()
        kernel = Kernel(
            id="kernel-123",
            name="python3",
            last_activity=now,
            execution_state="idle",
            connections=2
        )
        
        # Test conversion to dict
        data = kernel.model_dump()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["id"], "kernel-123")
        self.assertEqual(data["name"], "python3")
        self.assertEqual(data["execution_state"], "idle")
        self.assertEqual(data["connections"], 2)
        
    def test_kernel_model_from_api_response(self):
        """Test Kernel model creation from typical API response."""
        api_data = {
            "id": "f8b5c7a9-1234-5678-9abc-def012345678",
            "name": "python3", 
            "last_activity": "2023-12-01T10:30:15.123456Z",
            "execution_state": "busy",
            "connections": 3
        }
        
        kernel = Kernel(**api_data)
        
        self.assertEqual(kernel.id, "f8b5c7a9-1234-5678-9abc-def012345678")
        self.assertEqual(kernel.name, "python3")
        self.assertEqual(kernel.execution_state, "busy")
        self.assertEqual(kernel.connections, 3)

    def test_model_validation_errors(self):
        """Test model validation with invalid data."""
        # Test Kernel with missing required fields
        with self.assertRaises(ValueError):
            Kernel(id="test")  # Missing name

    def test_model_serialization(self):
        """Test model serialization to dict."""
        from datetime import datetime
        now = datetime.now()
        kernel = Kernel(
            id="kernel-123",
            name="python3",
            last_activity=now,
            execution_state="idle",
            connections=1
        )
        
        data = kernel.model_dump()
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data["id"], "kernel-123")
        self.assertEqual(data["name"], "python3")
        self.assertEqual(data["execution_state"], "idle")
        self.assertEqual(data["connections"], 1)


if __name__ == '__main__':
    unittest.main()
