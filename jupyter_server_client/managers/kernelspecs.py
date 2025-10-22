# Copyright (c) 2025 Datalayer, Inc.
#
# BSD 3-Clause License

"""KernelSpecs API manager for kernel specifications."""

from typing import Any

from jupyter_server_client.models import KernelSpecs


class KernelSpecsManager:
    """Manager for KernelSpecs API operations."""
    
    def __init__(self, http_client: Any):
        """Initialize kernel specs manager.
        
        Args:
            http_client: HTTP client instance
        """
        self.http_client = http_client
    
    def list_kernelspecs(self) -> KernelSpecs:
        """List all available kernel specifications.
        
        Returns:
            KernelSpecs object containing all kernel specs
        """
        response = self.http_client.get("/api/kernelspecs")
        return KernelSpecs(**response)
    
    def get_kernelspec(self, name: str) -> Any:
        """Get a specific kernel specification.
        
        Args:
            name: Kernel spec name
            
        Returns:
            Kernel specification details
        """
        kernelspecs = self.list_kernelspecs()
        return kernelspecs.kernelspecs.get(name)
    
    def get_default_kernelspec_name(self) -> str:
        """Get the name of the default kernel specification.
        
        Returns:
            Default kernel spec name
        """
        kernelspecs = self.list_kernelspecs()
        return kernelspecs.default
