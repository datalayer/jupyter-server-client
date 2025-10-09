# Copyright (c) 2025 Datalayer, Inc.
#
# BSD 3-Clause License

"""Jupyter Server Kernel Execute Manager.

This manager provides access to the undocumented /api/kernels/{kernel_id}/execute endpoint
that allows synchronous code execution and result retrieval.
"""

from typing import Any, Dict, Optional
import time

from jupyter_server_api.models import ExecutionRequest, ExecutionResult


class ExecsManager:
    """Manager for kernel code execution via Jupyter Server REST API.
    
    This provides access to an undocumented endpoint that allows synchronous
    code execution without requiring WebSocket connections.
    
    Note: This is an undocumented API and may change in future Jupyter Server versions.
    """

    def __init__(self, http_client):
        """Initialize execs manager.
        
        Args:
            http_client: HTTP client instance
        """
        self.http_client = http_client

    def execute(
        self,
        kernel_id: str,
        code: str,
        timeout: Optional[float] = None,
    ) -> ExecutionResult:
        """Execute code in a kernel and return the result.
        
        This method:
        1. POSTs code to /api/kernels/{kernel_id}/execute
        2. Extracts the Location header from the response
        3. Polls the result URL until execution completes
        
        Args:
            kernel_id: The ID of the kernel to execute code in
            code: Python code to execute
            timeout: Optional timeout in seconds for execution
            
        Returns:
            ExecutionResult with status, outputs, and execution count
            
        Raises:
            JupyterServerError: If the request fails
            JupyterTimeoutError: If execution times out
            ValueError: If Location header is missing
            
        Example:
            >>> execs = ExecsManager(http_client)
            >>> result = execs.execute(kernel_id, "print('Hello, World!')")
            >>> print(result.status)
            'ok'
            >>> print(result.outputs)
            [{'output_type': 'stream', 'name': 'stdout', 'text': 'Hello, World!\\n'}]
        """
        # Step 1: Submit execution request
        execution_request = ExecutionRequest(code=code)
        response = self._submit_execution(kernel_id, execution_request)
        
        # Step 2: Extract result URL from Location header
        result_url = self._extract_result_url(response)
        
        # Step 3: Poll for result
        result = self._poll_for_result(result_url, timeout)
        
        return result

    def _submit_execution(
        self,
        kernel_id: str,
        execution_request: ExecutionRequest,
    ) -> Any:
        """Submit code execution request.
        
        Args:
            kernel_id: Kernel ID
            execution_request: Execution request with code
            
        Returns:
            Raw response from the server
        """
        # We need to access the raw response to get headers
        # The standard post() method only returns parsed JSON
        # So we'll use the lower-level request() method
        url = f"/api/kernels/{kernel_id}/execute"
        
        # Make request and get raw response
        full_url = self.http_client._build_url(url)
        response = self.http_client.session.post(
            full_url,
            json=execution_request.model_dump(exclude_none=True),
            timeout=self.http_client.timeout,
        )
        
        # Check for errors
        if not response.ok:
            from jupyter_server_api.exceptions import create_error_from_response
            raise create_error_from_response(response)
        
        return response

    def _extract_result_url(self, response: Any) -> str:
        """Extract result URL from Location header.
        
        Args:
            response: HTTP response object
            
        Returns:
            Result URL path
            
        Raises:
            ValueError: If Location header is missing
        """
        location = response.headers.get('Location')
        if not location:
            raise ValueError("Location header not found in response")
        
        # Location header contains the path (e.g., /api/kernels/{id}/executions/{exec_id})
        return location

    def _poll_for_result(
        self,
        result_url: str,
        timeout: Optional[float] = None,
        poll_interval: float = 0.1,
    ) -> ExecutionResult:
        """Poll for execution result.
        
        Args:
            result_url: URL to poll for results
            timeout: Maximum time to wait in seconds (None = wait forever)
            poll_interval: Time between polls in seconds
            
        Returns:
            ExecutionResult when execution completes
            
        Raises:
            JupyterTimeoutError: If polling times out
        """
        start_time = time.time()
        
        while True:
            # Check timeout
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    from jupyter_server_api.exceptions import JupyterTimeoutError
                    raise JupyterTimeoutError(
                        f"Execution timed out after {timeout} seconds"
                    )
            
            # Poll for result
            response = self.http_client.get(result_url)
            
            # Check if execution is complete
            # The API returns the result when ready
            if response and 'status' in response:
                return ExecutionResult(**response)
            
            # Wait before next poll
            time.sleep(poll_interval)

    def get_execution_result(self, kernel_id: str, execution_id: str) -> ExecutionResult:
        """Get the result of a previously submitted execution.
        
        Args:
            kernel_id: The ID of the kernel
            execution_id: The ID of the execution
            
        Returns:
            ExecutionResult with status and outputs
            
        Raises:
            JupyterServerError: If the request fails
            
        Example:
            >>> execs = ExecsManager(http_client)
            >>> result = execs.get_execution_result(kernel_id, execution_id)
            >>> print(result.status)
            'ok'
        """
        url = f"/api/kernels/{kernel_id}/executions/{execution_id}"
        response = self.http_client.get(url)
        return ExecutionResult(**response)
