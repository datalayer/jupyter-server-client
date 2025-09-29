# Tests for jupyter-server-api

This directory contains comprehensive tests for the `jupyter-server-api` library.

## Test Structure

```
tests/
├── __init__.py              # Test package marker
├── conftest.py              # Test fixtures and configuration  
├── test_client.py           # Tests for main JupyterServerClient class
├── test_kernels.py          # Tests for KernelsManager (our main focus)
├── test_models.py           # Tests for Pydantic data models
├── test_http_client.py      # Tests for HTTP client functionality
├── test_integration.py      # Integration and workflow tests
├── requirements.txt         # Test dependencies
├── run_tests.py             # Test runner script
└── README.md               # This file
```

## Running Tests

### Method 1: Using the test runner script
```bash
# Run all tests
cd tests
python run_tests.py

# Run specific test module
python run_tests.py test_kernels
```

### Method 2: Using unittest directly
```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test file
python -m unittest tests.test_kernels -v

# Run specific test class
python -m unittest tests.test_kernels.TestKernelsManager -v

# Run specific test method
python -m unittest tests.test_kernels.TestKernelsManager.test_list_kernels_success -v
```

### Method 3: Using Make (if Makefile is available)
```bash
# Run all tests
make test

# Run tests with verbose output
make test-verbose

# Run specific test
make test-specific TEST=test_kernels

# Run with coverage
make test-coverage
```

## Test Categories

### 1. Unit Tests
- **test_client.py**: Tests the main `JupyterServerClient` class initialization and manager availability
- **test_kernels.py**: Tests the `KernelsManager` class, focusing on our core functionality
- **test_models.py**: Tests Pydantic data models for API response validation
- **test_http_client.py**: Tests HTTP client functionality (sync and async)

### 2. Integration Tests
- **test_integration.py**: Tests complete workflows and library separation of concerns

## Key Test Features

### Testing Our Core Functionality
The tests verify that our library provides:
- ✅ Kernel listing (`list_kernels()`)
- ✅ Individual kernel info (`get_kernel()`)
- ❌ **NO** kernel management (that's `jupyter-kernel-client`'s job)

### Separation of Concerns Testing
Our tests specifically verify that we:
1. **DON'T** duplicate `jupyter-kernel-client` functionality
2. **DON'T** duplicate `jupyter-nbmodel-client` functionality  
3. **DO** provide server-level operations and kernel listing

### Mock-Based Testing
All tests use mocks to avoid requiring:
- A running Jupyter server
- Network connectivity
- External dependencies

## Test Dependencies

### Required (built-in)
- `unittest` - Python's built-in testing framework
- `unittest.mock` - For mocking HTTP calls and responses

### Optional (install with pip)
```bash
pip install -r requirements.txt
```

- `coverage` - For test coverage reports
- `responses` - For more sophisticated HTTP mocking
- `flake8` - For code quality checks
- `black` - For code formatting

## Writing New Tests

When adding new functionality, follow these patterns:

### 1. Test File Structure
```python
import unittest
from unittest.mock import Mock, patch
from jupyter_server_api.your_module import YourClass

class TestYourClass(unittest.TestCase):
    def setUp(self):
        # Set up test fixtures
        pass
    
    def test_your_functionality(self):
        # Test your functionality
        pass
```

### 2. Mock HTTP Responses
```python
@patch('requests.get')
def test_api_call(self, mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"test": "data"}
    mock_get.return_value = mock_response
    
    # Your test code here
```

### 3. Test Separation of Concerns
Always include tests that verify we don't have functionality that belongs to other libraries:

```python
def test_no_forbidden_methods(self):
    forbidden_methods = ['start_kernel', 'delete_kernel']
    for method in forbidden_methods:
        self.assertFalse(hasattr(self.manager, method))
```

## Expected Test Results

When all tests pass, you should see:
- ✅ Client initialization works
- ✅ Kernel listing works (our main feature)
- ✅ No kernel management methods (proper separation)
- ✅ Data models validate correctly
- ✅ HTTP client handles requests properly
- ✅ Integration scenarios work as expected

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're running tests from the right directory
2. **Mock Failures**: Ensure you're patching the right module path
3. **Assertion Errors**: Check that expected vs actual data matches exactly

### Debug Mode
Run with Python's debug flag for more detailed error information:
```bash
python -u -m unittest tests.test_kernels -v
```
