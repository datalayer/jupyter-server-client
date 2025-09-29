# Copyright (c) 2025 Datalayer, Inc.
#
# BSD 3-Clause License

"""Jupyter Server Client - A Python client for Jupyter Server REST API."""

from jupyter_server_api.client import JupyterServerClient, AsyncJupyterServerClient
from jupyter_server_api.exceptions import (
    JupyterServerError,
    BadRequestError,
    ForbiddenError,
    NotFoundError,
    ServerError,
    AuthenticationError,
    JupyterConnectionError,
)
from jupyter_server_api.models import (
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
    "ForbiddenError",
    "NotFoundError",
    "ServerError",
    "AuthenticationError", 
    "JupyterConnectionError",
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
