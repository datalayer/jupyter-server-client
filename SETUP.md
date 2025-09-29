# Installation and Setup Guide

## Prerequisites

- Python 3.8 or higher
- A running Jupyter Server instance

## Installation

### From Source (Development)

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd jupyter-server-api
   ```

3. Install in development mode:
   ```bash
   pip install -e .
   ```

### From PyPI (Future)

```bash
pip install jupyter-server-api
```

## Setting up Jupyter Server

If you don't have a Jupyter Server running, you can start one:

### Option 1: Jupyter Lab
```bash
pip install jupyterlab
jupyter lab --port=8888
```

### Option 2: Jupyter Notebook
```bash
pip install notebook
jupyter notebook --port=8888
```

### Option 3: Jupyter Server (standalone)
```bash
pip install jupyter_server
jupyter server --port=8888
```

## Getting Your Token

When you start Jupyter Server, it will display a token in the terminal output. Look for something like:

```
http://127.0.0.1:8888/?token=abcd1234567890...
```

The token is the part after `token=`.

You can also get the token by running:
```bash
jupyter server list
```

## Quick Start

```python
from jupyter_server_api import JupyterServerClient

# Replace with your server URL and token
client = JupyterServerClient(
    base_url="http://localhost:8888",
    token="your-token-here"
)

# Get server information
server_info = client.get_version()
print(f"Server version: {server_info.version}")

# List notebooks
contents = client.contents.list_directory("")
print(f"Found {len(contents)} items")

# Close the client
client.close()
```

## Running Examples

1. Make sure Jupyter Server is running
2. Update the token in the example:
   ```bash
   export JUPYTER_TOKEN="your-token-here"
   python example.py
   ```

Or edit the `example.py` file directly to set your token.

## Testing

Run basic validation tests:
```bash
python test_basic.py
```

These tests don't require a running Jupyter Server and validate the library structure.

## Troubleshooting

### Connection Issues

1. **Server not running**: Make sure Jupyter Server is running on the specified port
2. **Wrong URL**: Check the URL and port number
3. **Invalid token**: Verify the token is correct
4. **Firewall**: Ensure the port is accessible

### Import Issues

1. **Module not found**: Make sure you installed the package (`pip install -e .`)
2. **Python path**: Ensure you're using the correct Python environment

### SSL Issues

If you get SSL certificate errors, you can disable SSL verification:
```python
client = JupyterServerClient(
    base_url="https://localhost:8888",
    token="your-token",
    verify_ssl=False  # Only for development!
)
```

## Environment Variables

You can use environment variables for configuration:

- `JUPYTER_SERVER_URL`: Base URL of the Jupyter Server
- `JUPYTER_TOKEN`: Authentication token

## Next Steps

- Read the [API Documentation](README.md#api-reference) for detailed usage
- Check the [example.py](example.py) for comprehensive examples
- Explore the source code in the `jupyter_server_api/` directory
