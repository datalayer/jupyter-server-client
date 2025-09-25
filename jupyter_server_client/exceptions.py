# Copyright (c) 2025 Datalayer, Inc.
#
# BSD 3-Clause License

"""Exception classes for Jupyter Server Client."""

from typing import Any, Dict, Optional, Union
import requests


class JupyterServerError(Exception):
    """Base exception for all Jupyter Server Client errors."""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Union[requests.Response, Dict[str, Any]]] = None,
        url: Optional[str] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response
        self.url = url
    
    def __str__(self) -> str:
        if self.status_code:
            return f"{self.status_code}: {self.message}"
        return self.message


class BadRequestError(JupyterServerError):
    """Exception raised for 400 Bad Request responses."""


class AuthenticationError(JupyterServerError):
    """Exception raised for 401 Unauthorized responses."""


class ForbiddenError(JupyterServerError):
    """Exception raised for 403 Forbidden responses."""


class NotFoundError(JupyterServerError):
    """Exception raised for 404 Not Found responses."""


class MethodNotAllowedError(JupyterServerError):
    """Exception raised for 405 Method Not Allowed responses."""


class ConflictError(JupyterServerError):
    """Exception raised for 409 Conflict responses."""


class ServerError(JupyterServerError):
    """Exception raised for 5xx Server Error responses."""


class JupyterConnectionError(JupyterServerError):
    """Exception raised when connection to Jupyter Server fails."""


class JupyterTimeoutError(JupyterServerError):
    """Exception raised when request times out."""


class ValidationError(JupyterServerError):
    """Exception raised when input validation fails."""


def create_error_from_response(
    response: requests.Response,
    message: Optional[str] = None,
) -> JupyterServerError:
    """Create an appropriate exception based on the HTTP response status code.
    
    Args:
        response: HTTP response object
        message: Optional custom error message
        
    Returns:
        Appropriate JupyterServerError subclass instance
    """
    if message is None:
        try:
            # Try to extract error message from response JSON
            error_data = response.json()
            if isinstance(error_data, dict):
                message = error_data.get("message") or error_data.get("error") or error_data.get("reason")
        except (ValueError, KeyError):
            pass
        
        if message is None:
            message = response.text or f"HTTP {response.status_code} error"
    
    # Choose exception class based on status code
    if response.status_code == 400:
        return BadRequestError(message, response.status_code, response, response.url)
    elif response.status_code == 401:
        return AuthenticationError(message, response.status_code, response, response.url)
    elif response.status_code == 403:
        return ForbiddenError(message, response.status_code, response, response.url)
    elif response.status_code == 404:
        return NotFoundError(message, response.status_code, response, response.url)
    elif response.status_code == 405:
        return MethodNotAllowedError(message, response.status_code, response, response.url)
    elif response.status_code == 409:
        return ConflictError(message, response.status_code, response, response.url)
    elif 500 <= response.status_code < 600:
        return ServerError(message, response.status_code, response, response.url)
    else:
        return JupyterServerError(message, response.status_code, response, response.url)
