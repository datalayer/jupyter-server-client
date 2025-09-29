# Copyright (c) 2025 Datalayer, Inc.
#
# BSD 3-Clause License

"""Jupyter Server Kernels Manager."""

from typing import Any, List

from jupyter_server_api.models import Kernel


class KernelsManager:
    """Manager for kernel listing via Jupyter Server REST API.
    
    Note: For kernel management operations (start, stop, restart, execute), 
    use jupyter-kernel-client which provides full kernel interaction capabilities.
    """

    def __init__(self, http_client):
        """Initialize kernels manager.
        
        Args:
            http_client: HTTP client instance
        """
        self.http_client = http_client

    def list_kernels(self) -> list[Kernel]:
        """List all running kernels on the server.
        
        This provides read-only information about running kernels.
        For kernel management operations, use jupyter-kernel-client.
        
        Returns:
            List of running kernel information
            
        Raises:
            JupyterServerError: If the request fails
        """
        response = self.http_client.get("/api/kernels")
        return [Kernel(**kernel_data) for kernel_data in response]

    def get_kernel(self, kernel_id: str) -> Kernel:
        """Get information about a specific kernel.
        
        This provides read-only information about a kernel.
        For kernel management operations, use jupyter-kernel-client.
        
        Args:
            kernel_id: The ID of the kernel to retrieve
            
        Returns:
            Kernel information
            
        Raises:
            JupyterServerError: If the request fails or kernel not found
        """
        response = self.http_client.get(f"/api/kernels/{kernel_id}")
        return Kernel(**response)
