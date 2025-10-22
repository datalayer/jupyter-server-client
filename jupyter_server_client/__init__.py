# Copyright (c) 2025 Datalayer, Inc.
#
# BSD 3-Clause License

"""Jupyter Server Client - A Python client for Jupyter Server REST API."""

from jupyter_server_client.client import AsyncJupyterServerClient, JupyterServerClient
from jupyter_server_client.exceptions import (
    JupyterServerError,
    BadRequestError,
    AuthenticationError,
    ForbiddenError,
    NotFoundError,
    MethodNotAllowedError,
    ConflictError,
    ServerError,
    JupyterConnectionError,
    JupyterTimeoutError,
    ValidationError,
)
from jupyter_server_client.models import (
    Contents,
    KernelInfo, 
    Session,
    Terminal,
    KernelSpec,
    KernelSpecs,
    Checkpoints,
    ServerInfo,
    APIStatus,
    Identity,
)

__version__ = "0.1.0"
__author__ = "Datalayer"
__email__ = "team@datalayer.io"

__all__ = [
    # Clients
    "JupyterServerClient",
    "AsyncJupyterServerClient",
    # Exceptions
    "JupyterServerError",
    "BadRequestError",
    "AuthenticationError",
    "ForbiddenError",
    "NotFoundError",
    "MethodNotAllowedError",
    "ConflictError",
    "ServerError",
    "JupyterConnectionError",
    "JupyterTimeoutError",
    "ValidationError",
    # Models
    "Contents",
    "KernelInfo",
    "Session", 
    "Terminal",
    "KernelSpec",
    "KernelSpecs",
    "Checkpoints",
    "ServerInfo",
    "APIStatus",
    "Identity",
]
