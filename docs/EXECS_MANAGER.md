# Kernel Execution Manager (ExecsManager)

## Overview

The `ExecsManager` provides access to an **undocumented** Jupyter Server API endpoint that allows synchronous code execution in kernels without requiring WebSocket connections. This is useful for simple script-based interactions with Jupyter kernels.

## ⚠️ Important Notes

- **This is an UNDOCUMENTED API** - The `/api/kernels/{kernel_id}/execute` endpoint is not officially documented and may change or be removed in future Jupyter Server versions.
- **Use with caution** - For production applications, consider using the official `jupyter-kernel-client` package which provides robust WebSocket-based kernel interaction.
- **Best for simple cases** - This API is ideal for simple, synchronous code execution scenarios where you don't need the full power of WebSocket-based kernel messaging.

## API Endpoint Pattern

The execution flow follows this pattern:

1. **Submit execution request**: `POST /api/kernels/{kernel_id}/execute`
   - Body: `{"code": "print('Hello')"}`
   - Returns: HTTP 201 Created with `Location` header

2. **Get result**: `GET {Location header path}`
   - Example: `GET /api/kernels/{kernel_id}/executions/{execution_id}`
   - Returns: `{"status": "ok", "execution_count": 1, "outputs": "[...]"}`

## Usage

### Basic Example

```python
from jupyter_server_api import JupyterServerClient

# Create client
client = JupyterServerClient(
    base_url="http://localhost:8888",
    token="your-token-here"
)

# Get a kernel ID (from existing kernel or create new session)
kernels = client.kernels.list_kernels()
kernel_id = kernels[0].id

# Execute code
result = client.execs.execute(kernel_id, "print('Hello, World!')")

print(f"Status: {result.status}")
print(f"Execution count: {result.execution_count}")
print(f"Outputs: {result.parsed_outputs}")
```

### Execute with Timeout

```python
# Execute with a 5-second timeout
result = client.execs.execute(
    kernel_id,
    "import time; time.sleep(2); print('Done!')",
    timeout=5.0
)
```

### Handle Errors

```python
try:
    result = client.execs.execute(kernel_id, "1 / 0")
    print(f"Status: {result.status}")  # Will be "error" if execution failed
    print(f"Outputs: {result.parsed_outputs}")  # Contains error traceback
except Exception as e:
    print(f"Execution failed: {e}")
```

### Access Previous Execution Results

```python
# If you have an execution ID from a previous execution
result = client.execs.get_execution_result(kernel_id, execution_id)
```

## API Reference

### ExecsManager

#### `execute(kernel_id: str, code: str, timeout: Optional[float] = None) -> ExecutionResult`

Execute code in a kernel and return the result.

**Parameters:**
- `kernel_id` (str): The ID of the kernel to execute code in
- `code` (str): Python code to execute
- `timeout` (float, optional): Maximum time to wait for execution (seconds). None = wait forever

**Returns:**
- `ExecutionResult`: Object containing status, outputs, and execution count

**Raises:**
- `JupyterServerError`: If the request fails
- `JupyterTimeoutError`: If execution times out
- `ValueError`: If Location header is missing from response

**Example:**
```python
result = client.execs.execute(
    kernel_id="abc-123",
    code="x = 42\nprint(x)",
    timeout=10.0
)
```

#### `get_execution_result(kernel_id: str, execution_id: str) -> ExecutionResult`

Get the result of a previously submitted execution.

**Parameters:**
- `kernel_id` (str): The ID of the kernel
- `execution_id` (str): The ID of the execution

**Returns:**
- `ExecutionResult`: Object containing status and outputs

**Example:**
```python
result = client.execs.get_execution_result("abc-123", "exec-456")
```

## Models

### ExecutionRequest

Request model for code execution.

**Fields:**
- `code` (str): Python code to execute
- `silent` (bool): Whether to execute silently (default: False)
- `store_history` (bool): Whether to store in history (default: True)
- `user_expressions` (dict, optional): User expressions to evaluate
- `allow_stdin` (bool): Whether to allow stdin (default: False)
- `stop_on_error` (bool): Whether to stop on error (default: True)

### ExecutionResult

Result model for code execution.

**Fields:**
- `status` (str): Execution status ("ok", "error", or "aborted")
- `execution_count` (int): Execution counter for this kernel
- `outputs` (str | list): Execution outputs (may be JSON string or parsed list)

**Properties:**
- `parsed_outputs` (list): Parsed outputs as list of dictionaries

**Example outputs:**
```python
result.parsed_outputs = [
    {
        "output_type": "stream",
        "name": "stdout",
        "text": "Hello, World!\n"
    }
]
```

## Output Types

The execution results can contain various output types:

### Stream Output
```json
{
    "output_type": "stream",
    "name": "stdout",
    "text": "Hello, World!\n"
}
```

### Execute Result (Display Data)
```json
{
    "output_type": "execute_result",
    "execution_count": 1,
    "data": {
        "text/plain": "42"
    },
    "metadata": {}
}
```

### Display Data (e.g., plots)
```json
{
    "output_type": "display_data",
    "data": {
        "image/png": "iVBORw0KGgoAAAA...",
        "text/plain": "<Figure size 640x480 with 1 Axes>"
    },
    "metadata": {}
}
```

### Error Output
```json
{
    "output_type": "error",
    "ename": "ZeroDivisionError",
    "evalue": "division by zero",
    "traceback": [
        "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
        "\u001b[0;31mZeroDivisionError\u001b[0m: division by zero"
    ]
}
```

## Comparison with jupyter-kernel-client

### Use ExecsManager when:
- ✅ You need simple, synchronous code execution
- ✅ You want to avoid WebSocket complexity
- ✅ You're building simple scripts or tools
- ✅ You don't need real-time kernel interaction

### Use jupyter-kernel-client when:
- ✅ You need full kernel lifecycle management (start, stop, restart)
- ✅ You need real-time output streaming
- ✅ You need to interrupt running code
- ✅ You need stdin support for interactive input
- ✅ You're building production applications
- ✅ You need Widget/Comm support

## Testing with curl

You can test the endpoint directly with curl:

```bash
# Start a kernel (via session or kernels endpoint)
# Assume kernel ID is stored in $KERNEL_ID

# Execute code
RESPONSE=$(curl --include http://localhost:8888/api/kernels/$KERNEL_ID/execute \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"1+1=\", 1+1)"}')

# Extract result URL from Location header
RESULT_PATH=$(echo "$RESPONSE" | grep -oP 'Location:\s*\K[^ ]+' | tr -d '\r\n')

# Get result
curl "http://localhost:8888${RESULT_PATH}" \
  -H "Authorization: Bearer $TOKEN"
```

## Implementation Notes

### Polling Mechanism

The `execute()` method polls the result URL until execution completes:
- Default poll interval: 0.1 seconds
- Continues until result has 'status' field
- Respects timeout parameter if provided

### Error Handling

The manager handles several error scenarios:
- Missing Location header → `ValueError`
- HTTP errors → `JupyterServerError`
- Timeouts → `JupyterTimeoutError`
- Connection errors → `JupyterConnectionError`

### Thread Safety

The ExecsManager is **not thread-safe**. If you need concurrent execution:
- Create separate client instances per thread
- Or use external synchronization (locks)
- Or use jupyter-kernel-client with async support

## Limitations

1. **No real-time streaming** - You get all outputs at once after execution completes
2. **No stdin support** - Cannot interact with code that requests user input
3. **No interruption** - Cannot interrupt running code (must wait for timeout)
4. **No kernel management** - Cannot start/stop kernels (use sessions or kernels endpoints)
5. **Undocumented** - API may change without notice

## Future Considerations

If this API becomes officially documented, we should:
1. Add more comprehensive tests
2. Add async support
3. Add progress callbacks
4. Add support for execution options (silent, store_history, etc.)
5. Add support for user_expressions

## See Also

- [Jupyter Server REST API Documentation](https://jupyter-server.readthedocs.io/en/latest/developers/rest-api.html)
- [jupyter-kernel-client](https://github.com/datalayer/jupyter-kernel-client) - For full kernel interaction
- [Example script](./example_execs.py) - Complete working example
