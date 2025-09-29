# Copyright (c) 2025 Datalayer, Inc.
#
# BSD 3-Clause License

"""Data models for Jupyter Server API responses."""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict


class JupyterModel(BaseModel):
    """Base model for all Jupyter Server API models."""
    model_config = ConfigDict(extra="allow", validate_assignment=True)


class Contents(JupyterModel):
    """Model for file/directory contents from the Contents API."""
    
    name: str = Field(..., description="Name of file or directory")
    path: str = Field(..., description="Full path for file or directory")
    type: str = Field(..., description="Type of content (file, directory, notebook)")
    writable: bool = Field(..., description="Whether the file can be edited")
    created: datetime = Field(..., description="Creation timestamp")
    last_modified: datetime = Field(..., description="Last modified timestamp")
    mimetype: Optional[str] = Field(None, description="MIME type of the file")
    content: Optional[Union[str, List[Dict[str, Any]], Dict[str, Any]]] = Field(
        None, description="The file content"
    )
    format: Optional[str] = Field(None, description="Format of content")
    size: Optional[int] = Field(None, description="Size of file in bytes")
    hash: Optional[str] = Field(None, description="Hash of file content")
    hash_algorithm: Optional[str] = Field(None, description="Hash algorithm used")


class KernelInfo(JupyterModel):
    """Basic kernel information for sessions (full kernel management via jupyter-kernel-client)."""
    
    id: str = Field(..., description="Unique kernel ID")
    name: str = Field(..., description="Kernel spec name")


class Kernel(JupyterModel):
    """Model for running kernel information."""
    
    id: str = Field(..., description="Unique kernel ID")
    name: str = Field(..., description="Kernel spec name")
    last_activity: datetime = Field(..., description="Last activity timestamp")
    execution_state: str = Field(..., description="Kernel execution state")
    connections: int = Field(..., description="Number of connections to this kernel")


class Session(JupyterModel):
    """Model for session information."""
    
    id: str = Field(..., description="Unique session ID")
    path: str = Field(..., description="Path to the session file")
    name: Optional[str] = Field(None, description="Name of the session")
    type: str = Field(..., description="Session type (notebook, file, etc.)")
    kernel: Optional[KernelInfo] = Field(None, description="Associated kernel info")


class Terminal(JupyterModel):
    """Model for terminal information."""
    
    name: str = Field(..., description="Terminal name/ID")
    last_activity: Optional[datetime] = Field(None, description="Last activity timestamp")


class KernelSpecDetails(JupyterModel):
    """Model for kernel specification details (inside 'spec' field)."""
    
    display_name: str = Field(..., description="Display name for the kernel")
    language: str = Field(..., description="Programming language")
    argv: List[str] = Field(..., description="Command line arguments to start kernel")
    env: Optional[Dict[str, str]] = Field(None, description="Environment variables")
    interrupt_mode: Optional[str] = Field(None, description="Interrupt mode")
    codemirror_mode: Optional[Union[str, Dict[str, Any]]] = Field(
        None, description="CodeMirror mode"
    )
    help_links: Optional[List[Dict[str, str]]] = Field(None, description="Help links")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class KernelSpec(JupyterModel):
    """Model for kernel specification information."""
    
    name: str = Field(..., description="Kernel spec name")
    spec: KernelSpecDetails = Field(..., description="Kernel specification details")
    resources: Optional[Dict[str, str]] = Field(None, description="Kernel resources (logos, etc.)")


class KernelSpecs(JupyterModel):
    """Model for kernel specs collection."""
    
    default: str = Field(..., description="Default kernel spec name")
    kernelspecs: Dict[str, KernelSpec] = Field(..., description="Available kernel specs")


class Checkpoints(JupyterModel):
    """Model for file checkpoint information."""
    
    id: str = Field(..., description="Checkpoint ID")
    last_modified: datetime = Field(..., description="Last modified timestamp")


class APIStatus(JupyterModel):
    """Model for server status information."""
    
    started: Optional[datetime] = Field(None, description="Server start timestamp")
    last_activity: Optional[datetime] = Field(None, description="Last activity timestamp")
    connections: Optional[int] = Field(None, description="Total connections")
    kernels: Optional[int] = Field(None, description="Number of running kernels")


class Identity(JupyterModel):
    """Model for user identity information."""
    
    username: Optional[str] = Field(None, description="Username")
    name: Optional[str] = Field(None, description="Full name")
    display_name: Optional[str] = Field(None, description="Display name")
    initials: Optional[str] = Field(None, description="User initials")
    avatar_url: Optional[str] = Field(None, description="Avatar image URL")
    color: Optional[str] = Field(None, description="User color")


class ServerInfo(JupyterModel):
    """Model for server version information."""
    
    version: str = Field(..., description="Jupyter Server version")


class ErrorResponse(JupyterModel):
    """Model for error responses."""
    
    error: Optional[str] = Field(None, description="Error message")
    message: Optional[str] = Field(None, description="Detailed error message")
    reason: Optional[str] = Field(None, description="Error reason")
    traceback: Optional[str] = Field(None, description="Error traceback")
