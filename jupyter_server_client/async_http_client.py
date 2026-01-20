# Copyright (c) 2025 Datalayer, Inc.
#
# BSD 3-Clause License

"""Async HTTP client utilities for Jupyter Server Client."""

import json
from typing import Any, Dict, Optional

from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPClientError

from jupyter_server_client.exceptions import (
    JupyterConnectionError,
    JupyterTimeoutError,
    JupyterNotFoundError,
    JupyterAuthenticationError,
    JupyterServerError,
)


class AsyncBaseHTTPClient:
    """Async HTTP client for Jupyter Server API using Tornado."""
    
    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 30.0,
        verify_ssl: bool = True,
        user_agent: str = "jupyter-server-client/0.1.0",
    ):
        """Initialize async HTTP client.
        
        Args:
            base_url: Base URL of Jupyter Server
            token: Authentication token
            headers: Additional HTTP headers
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            user_agent: User agent string
        """
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.user_agent = user_agent
        self._additional_headers = headers or {}
        
        self._http_client = AsyncHTTPClient()
    
    def _build_url(self, path: str) -> str:
        """Build full URL from base URL and path."""
        return f"{self.base_url}/{path.lstrip('/')}"
    
    def _get_headers(self, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Build request headers with authentication."""
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": self.user_agent,
        }
        
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        headers.update(self._additional_headers)
        
        if additional_headers:
            headers.update(additional_headers)
        
        return headers
    
    def _handle_error(self, error: HTTPClientError, url: str) -> None:
        """Convert HTTP errors to appropriate exceptions."""
        if error.code == 401:
            raise JupyterAuthenticationError(f"Authentication failed for {url}")
        elif error.code == 403:
            raise JupyterAuthenticationError(f"Access forbidden for {url}")
        elif error.code == 404:
            raise JupyterNotFoundError(f"Resource not found: {url}")
        elif error.code >= 500:
            raise JupyterServerError(f"Server error ({error.code}) for {url}: {error.message}")
        else:
            raise JupyterServerError(f"HTTP error ({error.code}) for {url}: {error.message}")
    
    async def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        body: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> tuple[int, Dict[str, str], Any]:
        """Make async HTTP request to Jupyter Server.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            path: API path (will be joined with base_url)
            params: URL parameters
            json_data: JSON data to send
            body: Raw body bytes to send
            headers: Additional headers
            timeout: Request timeout (overrides default)
            
        Returns:
            Tuple of (status_code, response_headers, response_data)
            
        Raises:
            JupyterServerError: For various HTTP errors
            JupyterConnectionError: For connection issues
            JupyterTimeoutError: For timeout issues
        """
        url = self._build_url(path)
        
        if params:
            query_string = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{url}?{query_string}"
        
        request_headers = self._get_headers(headers)
        request_timeout = timeout or self.timeout
        
        # Prepare body
        request_body = None
        if json_data is not None:
            request_body = json.dumps(json_data).encode("utf-8")
        elif body is not None:
            request_body = body
        
        try:
            request = HTTPRequest(
                url,
                method=method,
                headers=request_headers,
                body=request_body if method in ("POST", "PUT", "PATCH") else None,
                request_timeout=request_timeout,
                validate_cert=self.verify_ssl,
            )
            
            response = await self._http_client.fetch(request)
            
            # Parse response
            response_data = None
            if response.body:
                try:
                    response_data = json.loads(response.body)
                except json.JSONDecodeError:
                    response_data = response.body
            
            return response.code, dict(response.headers), response_data
            
        except HTTPClientError as e:
            if e.code == 599:  # Timeout
                raise JupyterTimeoutError(f"Request timeout to {url}")
            self._handle_error(e, url)
        except Exception as e:
            if "timeout" in str(e).lower():
                raise JupyterTimeoutError(f"Request timeout to {url}")
            raise JupyterConnectionError(f"Connection error to {url}: {e}")
    
    async def request_raw(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        body: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> tuple[int, Dict[str, str], bytes]:
        """Make async HTTP request and return raw response.
        
        Similar to request() but returns raw bytes instead of parsed JSON.
        Useful for proxying responses without modification.
        
        Returns:
            Tuple of (status_code, response_headers, response_body_bytes)
        """
        url = self._build_url(path)
        
        if params:
            query_string = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{url}?{query_string}"
        
        request_headers = self._get_headers(headers)
        request_timeout = timeout or self.timeout
        
        # Prepare body
        request_body = None
        if json_data is not None:
            request_body = json.dumps(json_data).encode("utf-8")
        elif body is not None:
            request_body = body
        
        try:
            request = HTTPRequest(
                url,
                method=method,
                headers=request_headers,
                body=request_body if method in ("POST", "PUT", "PATCH") else None,
                request_timeout=request_timeout,
                validate_cert=self.verify_ssl,
            )
            
            response = await self._http_client.fetch(request, raise_error=False)
            return response.code, dict(response.headers), response.body or b""
            
        except Exception as e:
            if "timeout" in str(e).lower():
                raise JupyterTimeoutError(f"Request timeout to {url}")
            raise JupyterConnectionError(f"Connection error to {url}: {e}")
    
    async def get(self, path: str, **kwargs: Any) -> tuple[int, Dict[str, str], Any]:
        """Make async GET request."""
        return await self.request("GET", path, **kwargs)
    
    async def post(self, path: str, **kwargs: Any) -> tuple[int, Dict[str, str], Any]:
        """Make async POST request."""
        return await self.request("POST", path, **kwargs)
    
    async def put(self, path: str, **kwargs: Any) -> tuple[int, Dict[str, str], Any]:
        """Make async PUT request."""
        return await self.request("PUT", path, **kwargs)
    
    async def patch(self, path: str, **kwargs: Any) -> tuple[int, Dict[str, str], Any]:
        """Make async PATCH request."""
        return await self.request("PATCH", path, **kwargs)
    
    async def delete(self, path: str, **kwargs: Any) -> tuple[int, Dict[str, str], Any]:
        """Make async DELETE request."""
        return await self.request("DELETE", path, **kwargs)
    
    async def get_raw(self, path: str, **kwargs: Any) -> tuple[int, Dict[str, str], bytes]:
        """Make async GET request returning raw response."""
        return await self.request_raw("GET", path, **kwargs)
    
    async def post_raw(self, path: str, **kwargs: Any) -> tuple[int, Dict[str, str], bytes]:
        """Make async POST request returning raw response."""
        return await self.request_raw("POST", path, **kwargs)
    
    async def delete_raw(self, path: str, **kwargs: Any) -> tuple[int, Dict[str, str], bytes]:
        """Make async DELETE request returning raw response."""
        return await self.request_raw("DELETE", path, **kwargs)
    
    async def patch_raw(self, path: str, **kwargs: Any) -> tuple[int, Dict[str, str], bytes]:
        """Make async PATCH request returning raw response."""
        return await self.request_raw("PATCH", path, **kwargs)
