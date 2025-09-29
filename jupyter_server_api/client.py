# Copyright (c) 2025 Datalayer, Inc.
#
# BSD 3-Clause License

"""Main client classes for Jupyter Server API."""

from typing import Any, Dict, Optional

from jupyter_server_api.http_client import BaseHTTPClient
from jupyter_server_api.managers import (
    ContentsManager,
    SessionsManager, 
    TerminalsManager,
    KernelSpecsManager,
    KernelsManager,
)
from jupyter_server_api.models import ServerInfo, APIStatus, Identity


class JupyterServerClient:
    """Synchronous client for Jupyter Server REST API."""
    
    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 30.0,
        verify_ssl: bool = True,
        user_agent: str = "jupyter-server-client/0.1.0",
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """Initialize Jupyter Server client.
        
        Args:
            base_url: Base URL of Jupyter Server (e.g., 'http://localhost:8888')
            token: Authentication token
            headers: Additional HTTP headers
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            user_agent: User agent string
            max_retries: Maximum number of retries for failed requests
            retry_delay: Delay between retries in seconds
        """
        self.http_client = BaseHTTPClient(
            base_url=base_url,
            token=token,
            headers=headers,
            timeout=timeout,
            verify_ssl=verify_ssl,
            user_agent=user_agent,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )
        
        # Initialize API managers
        self.contents = ContentsManager(self.http_client)
        self.sessions = SessionsManager(self.http_client)
        self.terminals = TerminalsManager(self.http_client)
        self.kernelspecs = KernelSpecsManager(self.http_client)
        self.kernels = KernelsManager(self.http_client)
    
    def get_version(self) -> ServerInfo:
        """Get Jupyter Server version information.
        
        Returns:
            ServerInfo object with version information
        """
        response = self.http_client.get("/api/")
        return ServerInfo(**response)
    
    def get_status(self) -> APIStatus:
        """Get server status information.
        
        Returns:
            APIStatus object with server status
        """
        response = self.http_client.get("/api/status")
        return APIStatus(**response)
    
    def get_identity(self, permissions: Optional[Dict[str, Any]] = None) -> Identity:
        """Get current user identity and permissions.
        
        Args:
            permissions: Dictionary of permissions to check
            
        Returns:
            Identity object with user information
        """
        params = {}
        if permissions:
            import json
            params["permissions"] = json.dumps(permissions)
        
        response = self.http_client.get("/api/me", params=params)
        return Identity(**response.get("identity", {}))
    
    def get_api_spec(self) -> str:
        """Get OpenAPI specification for the server.
        
        Returns:
            YAML string of the API specification
        """
        return self.http_client.get("/api/spec.yaml")
    
    def close(self) -> None:
        """Close the client connection."""
        self.http_client.close()
    
    def __enter__(self) -> "JupyterServerClient":
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()


# For now, the async client will be a placeholder pointing to the sync client
# In a full implementation, this would use aiohttp instead of requests
class AsyncJupyterServerClient:
    """Asynchronous client for Jupyter Server REST API."""
    
    def __init__(self, *args: Any, **kwargs: Any):
        """Initialize async client.
        
        Note: This is a placeholder implementation.
        In a full implementation, this would use aiohttp for async operations.
        """
        raise NotImplementedError(
            "Async client not yet implemented. "
            "Use JupyterServerClient for synchronous operations."
        )
    
    async def __aenter__(self) -> "AsyncJupyterServerClient":
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        return None
