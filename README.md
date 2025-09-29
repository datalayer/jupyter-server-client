<!--
  ~ Copyright (c) 2025 Datalayer, Inc.
  ~
  ~ BSD 3-Clause License
-->

[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.io)

[![Become a Sponsor](https://img.shields.io/static/v1?label=Become%20a%20Sponsor&message=%E2%9D%A4&logo=GitHub&style=flat&color=1ABC9C)](https://github.com/sponsors/datalayer)

# 🪐 Jupyter Server Client

[![Github Actions Status](https://github.com/datalayer/jupyter-server-api/workflows/Build/badge.svg)](https://github.com/datalayer/jupyter-server-api/actions/workflows/build.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/jupyter-server-api)](https://pypi.org/project/jupyter-server-api)

`Jupyter Server Client` is a Python library to interact with Jupyter Server REST API for server management operations. It provides server-level functionality including kernel listing (read-only) while avoiding duplication with existing kernel management libraries.

## Complementary Libraries

This library works alongside existing Datalayer clients:
- **[jupyter-nbmodel-client](https://github.com/datalayer/jupyter-nbmodel-client)**: Real-time notebook collaboration and editing
- **[jupyter-kernel-client](https://github.com/datalayer/jupyter-kernel-client)**: Kernel management and code execution

## Features

- **Contents Management**: File and directory operations (create, read, update, delete)
- **Session Management**: Notebook-kernel session handling
- **Kernel Listing**: List and inspect running kernels (read-only)
- **Server Status**: Server information and health monitoring  
- **Terminal Management**: Server terminal operations
- **KernelSpec Info**: Available kernel specifications discovery
- **Authentication**: Token-based authentication support

## Installation

To install the library, run the following command:

```bash
pip install jupyter_server_api
```

## Quick Start

### Complete Integration Example

See [integration_example.py](integration_example.py) for a comprehensive example showing how all three libraries work together.

### Context Manager

```python
from jupyter_server_api import JupyterServerClient

# Server and content management
with JupyterServerClient("http://localhost:8888", token="your-token") as client:
    # Server information
    server_info = client.get_version()
    print(f"Server version: {server_info.version}")
    
    # Contents management
    notebook = client.contents.create_notebook("my_notebook.ipynb")
    contents = client.contents.list_directory("")
    
    # Session management
    session = client.sessions.create_session("my_notebook.ipynb")
    
    # Available kernelspecs
    kernelspecs = client.kernelspecs.list_kernelspecs()
    
    # List running kernels (read-only)
    kernels = client.kernels.list_kernels()
    for kernel in kernels:
        print(f"Kernel {kernel.id}: {kernel.name} ({kernel.execution_state})")
```

### Integration with Other Datalayer Clients

```python
# Kernel management and execution (jupyter-kernel-client)
from jupyter_kernel_client import KernelClient

with KernelClient(server_url="http://localhost:8888", token="your-token") as kernel:
    result = kernel.execute("print('Hello from kernel!')")
    print(f"Status: {result['status']}")

# Real-time notebook collaboration (jupyter-nbmodel-client)  
from jupyter_nbmodel_client import NbModelClient, get_jupyter_notebook_websocket_url
from jupyter_kernel_client import KernelClient

ws_url = get_jupyter_notebook_websocket_url(
    server_url="http://localhost:8888",
    token="your-token", 
    path="notebook.ipynb"
)

with KernelClient(server_url="http://localhost:8888", token="your-token") as kernel:
    async with NbModelClient(ws_url) as notebook:
        cell_index = notebook.add_code_cell("print('Collaborative!')")
        results = notebook.execute_cell(cell_index, kernel)
```

### Async Support

The client also supports async operations:

```python
import asyncio
from jupyter_server_api import AsyncJupyterServerClient

async def main():
    async with AsyncJupyterServerClient(
        base_url="http://localhost:8888",
        token="your-server-token"
    ) as client:
        # All operations are async
        notebook = await client.contents.create_notebook("async-notebook.ipynb")
        kernel = await client.kernels.start_kernel(name="python3")
        
        # List resources
        kernels = await client.kernels.list_kernels()
        sessions = await client.sessions.list_sessions()

asyncio.run(main())
```

## API Reference

### Contents API

```python
# Create a new notebook
notebook = client.contents.create_notebook("path/to/notebook.ipynb")

# Create a directory
directory = client.contents.create_directory("path/to/directory")

# Get contents (file or directory)
contents = client.contents.get("path/to/file.ipynb")

# Save/update a notebook
updated = client.contents.save_notebook(
    path="path/to/notebook.ipynb",
    content=notebook_content
)

# List directory contents
files = client.contents.list_directory("path/to/directory")

# Rename a file/directory
renamed = client.contents.rename("old/path.ipynb", "new/path.ipynb")

# Delete a file/directory
client.contents.delete("path/to/file.ipynb")

# Copy a file
copy = client.contents.copy_file(
    from_path="source.ipynb", 
    to_path="destination.ipynb"
)
```

### Kernels API

```python
# List all kernels
kernels = client.kernels.list_kernels()

# Start a new kernel
kernel = client.kernels.start_kernel(
    name="python3",  # kernel spec name
    path="/path/to/working/directory"  # optional working directory
)

# Get kernel information
info = client.kernels.get_kernel(kernel_id)

# Restart a kernel
restarted = client.kernels.restart_kernel(kernel_id)

# Interrupt a kernel
client.kernels.interrupt_kernel(kernel_id)

# Delete/stop a kernel
client.kernels.delete_kernel(kernel_id)
```

### Sessions API

```python
# List all sessions
sessions = client.sessions.list_sessions()

# Create a new session
session = client.sessions.create_session(
    path="notebook.ipynb",
    kernel={'name': 'python3'},
    type="notebook",
    name="My Session"
)

# Get session details
session = client.sessions.get_session(session_id)

# Update a session (rename)
updated = client.sessions.update_session(
    session_id=session_id,
    path="new-path.ipynb",
    name="New Session Name"
)

# Delete a session
client.sessions.delete_session(session_id)
```

### Terminals API

```python
# List all terminals
terminals = client.terminals.list_terminals()

# Create a new terminal
terminal = client.terminals.create_terminal()

# Get terminal information
info = client.terminals.get_terminal(terminal_name)

# Delete a terminal
client.terminals.delete_terminal(terminal_name)
```

### Server Info

```python
# Get server version
version = client.get_version()

# Get server status
status = client.get_status()

# Get current user identity
identity = client.get_identity()

# Get kernel specs
kernelspecs = client.kernelspecs.list_kernelspecs()
```

## Error Handling

The client provides specific exceptions for different types of errors:

```python
from jupyter_server_api import (
    JupyterServerClient, 
    JupyterServerError,
    NotFoundError,
    ForbiddenError,
    BadRequestError
)

try:
    client = JupyterServerClient("http://localhost:8888", token="invalid")
    notebook = client.contents.get("nonexistent.ipynb")
except NotFoundError as e:
    print(f"File not found: {e}")
except ForbiddenError as e:
    print(f"Access denied: {e}")
except JupyterServerError as e:
    print(f"Server error: {e}")
```

## Configuration

You can configure the client behavior:

```python
from jupyter_server_api import JupyterServerClient

client = JupyterServerClient(
    base_url="http://localhost:8888",
    token="your-token",
    timeout=30,  # Request timeout in seconds
    verify_ssl=True,  # SSL verification
    user_agent="MyApp/1.0",  # Custom user agent
    max_retries=3,  # Number of retries on failure
    retry_delay=1.0  # Delay between retries
)
```

## Authentication

The client supports multiple authentication methods:

```python
# Token-based authentication (recommended)
client = JupyterServerClient(
    base_url="http://localhost:8888",
    token="your-server-token"
)

# No authentication (for local development)
client = JupyterServerClient(base_url="http://localhost:8888")

# Custom headers
client = JupyterServerClient(
    base_url="http://localhost:8888",
    headers={
        "Authorization": "Bearer your-token",
        "Custom-Header": "value"
    }
)
```

## Development Setup

### Installation

```bash
# Clone the repository
git clone https://github.com/datalayer/jupyter-server-api.git
cd jupyter-server-api

# Install in development mode
pip install -e ".[test,lint,typing]"
```

### Running Tests

```bash
# Install test dependencies
pip install -e ".[test]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=jupyter_server_api --cov-report=html
```

### Code Quality

```bash
# Install linting tools
pip install -e ".[lint]"

# Run linting
ruff check .
ruff format .

# Type checking
mypy jupyter_server_api
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## Related Projects

- [jupyter-nbmodel-client](https://github.com/datalayer/jupyter-nbmodel-client) - Client for real-time collaborative Jupyter notebooks
- [Jupyter Server](https://github.com/jupyter-server/jupyter_server) - The backend for Jupyter web applications
- [JupyterLab](https://github.com/jupyterlab/jupyterlab) - An extensible environment for interactive computing
