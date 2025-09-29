# Copyright (c) 2025 Datalayer, Inc.
#
# BSD 3-Clause License

"""HTTP client utilities for Jupyter Server Client."""

import json
import time
from typing import Any, Dict, Optional, Union
from urllib.parse import urljoin, urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from jupyter_server_client.exceptions import (
    JupyterConnectionError,
    JupyterTimeoutError,
    create_error_from_response,
)


class BaseHTTPClient:
    """Base HTTP client for Jupyter Server API."""
    
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
        """Initialize HTTP client.
        
        Args:
            base_url: Base URL of Jupyter Server
            token: Authentication token
            headers: Additional HTTP headers
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            user_agent: User agent string
            max_retries: Maximum number of retries
            retry_delay: Delay between retries
        """
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Set up session
        self.session = requests.Session()
        
        # Configure retries
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=retry_delay,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set headers
        default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": user_agent,
        }
        
        if token:
            default_headers["Authorization"] = f"Bearer {token}"
        
        if headers:
            default_headers.update(headers)
        
        self.session.headers.update(default_headers)
        
        # SSL verification
        self.session.verify = verify_ssl
    
    def _build_url(self, path: str) -> str:
        """Build full URL from base URL and path."""
        return urljoin(self.base_url, path.lstrip("/"))
    
    def _handle_response(self, response: requests.Response) -> Any:
        """Handle HTTP response and raise appropriate exceptions."""
        if response.ok:
            if response.status_code == 204:  # No Content
                return None
            
            # Try to parse JSON response
            try:
                return response.json()
            except json.JSONDecodeError:
                return response.text
        else:
            # Raise appropriate exception based on status code
            raise create_error_from_response(response)
    
    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """Make HTTP request to Jupyter Server.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            path: API path (will be joined with base_url)
            params: URL parameters
            data: Form data
            json_data: JSON data
            headers: Additional headers
            timeout: Request timeout (overrides default)
            
        Returns:
            Response data
            
        Raises:
            JupyterServerError: For various HTTP errors
            JupyterConnectionError: For connection issues
            JupyterTimeoutError: For timeout issues
        """
        url = self._build_url(path)
        request_timeout = timeout or self.timeout
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                headers=headers,
                timeout=request_timeout,
            )
            return self._handle_response(response)
            
        except requests.exceptions.ConnectTimeout:
            raise JupyterTimeoutError(f"Connection timeout to {url}")
        except requests.exceptions.ReadTimeout:
            raise JupyterTimeoutError(f"Read timeout from {url}")
        except requests.exceptions.Timeout:
            raise JupyterTimeoutError(f"Request timeout to {url}")
        except requests.exceptions.ConnectionError as e:
            raise JupyterConnectionError(f"Connection error to {url}: {e}")
        except requests.exceptions.RequestException as e:
            raise JupyterConnectionError(f"Request error to {url}: {e}")
    
    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Make GET request."""
        return self.request("GET", path, params=params, **kwargs)
    
    def post(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Make POST request."""
        return self.request("POST", path, json_data=json_data, data=data, **kwargs)
    
    def put(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Make PUT request."""
        return self.request("PUT", path, json_data=json_data, data=data, **kwargs)
    
    def patch(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Make PATCH request."""
        return self.request("PATCH", path, json_data=json_data, data=data, **kwargs)
    
    def delete(
        self,
        path: str,
        **kwargs: Any,
    ) -> Any:
        """Make DELETE request."""
        return self.request("DELETE", path, **kwargs)
    
    def close(self) -> None:
        """Close the HTTP session."""
        if self.session:
            self.session.close()
    
    def __enter__(self) -> "BaseHTTPClient":
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()
