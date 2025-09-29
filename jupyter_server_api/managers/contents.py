# Copyright (c) 2025 Datalayer, Inc.
#
# BSD 3-Clause License

"""Contents API manager for file and directory operations."""

import json
from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote

from jupyter_server_api.models import Contents


class ContentsManager:
    """Manager for Contents API operations."""
    
    def __init__(self, http_client: Any):
        """Initialize contents manager.
        
        Args:
            http_client: HTTP client instance
        """
        self.http_client = http_client
    
    def get(
        self,
        path: str,
        type: Optional[str] = None,
        format: Optional[str] = None,
        content: Optional[bool] = None,
        hash_content: Optional[bool] = None,
    ) -> Contents:
        """Get contents of file or directory.
        
        Args:
            path: File or directory path
            type: Content type filter ('file', 'directory', 'notebook')
            format: Content format ('text', 'base64', 'json')
            content: Whether to include content (default: True)
            hash_content: Whether to include content hash
            
        Returns:
            Contents object
        """
        params: Dict[str, Any] = {}
        if type is not None:
            params["type"] = type
        if format is not None:
            params["format"] = format
        if content is not None:
            params["content"] = int(content)
        if hash_content is not None:
            params["hash"] = int(hash_content)
        
        encoded_path = quote(path, safe="/")
        response = self.http_client.get(f"/api/contents/{encoded_path}", params=params)
        return Contents(**response)
    
    def list_directory(self, path: str = "") -> List[Contents]:
        """List contents of a directory.
        
        Args:
            path: Directory path (empty for root)
            
        Returns:
            List of Contents objects
        """
        contents = self.get(path, type="directory", content=True)
        if contents.content and isinstance(contents.content, list):
            return [Contents(**item) for item in contents.content]
        return []
    
    def create_notebook(
        self,
        path: str,
        content: Optional[Dict[str, Any]] = None,
    ) -> Contents:
        """Create a new notebook.
        
        Args:
            path: Path for the new notebook
            content: Notebook content (optional, will create empty notebook if not provided)
            
        Returns:
            Contents object for created notebook
        """
        if content is None:
            # Create empty notebook structure
            content = {
                "cells": [],
                "metadata": {},
                "nbformat": 4,
                "nbformat_minor": 4,
            }
        
        data = {
            "type": "notebook",
            "format": "json",
            "content": content,
        }
        
        encoded_path = quote(path, safe="/")
        response = self.http_client.put(f"/api/contents/{encoded_path}", json_data=data)
        return Contents(**response)
    
    def create_file(
        self,
        path: str,
        content: str = "",
        format: str = "text",
    ) -> Contents:
        """Create a new file.
        
        Args:
            path: Path for the new file
            content: File content
            format: Content format ('text', 'base64')
            
        Returns:
            Contents object for created file
        """
        data = {
            "type": "file",
            "format": format,
            "content": content,
        }
        
        encoded_path = quote(path, safe="/")
        response = self.http_client.put(f"/api/contents/{encoded_path}", json_data=data)
        return Contents(**response)
    
    def create_directory(self, path: str) -> Contents:
        """Create a new directory.
        
        Args:
            path: Path for the new directory
            
        Returns:
            Contents object for created directory
        """
        data = {"type": "directory"}
        
        encoded_path = quote(path, safe="/")
        response = self.http_client.put(f"/api/contents/{encoded_path}", json_data=data)
        return Contents(**response)
    
    def save_notebook(
        self,
        path: str,
        content: Dict[str, Any],
        format: str = "json",
    ) -> Contents:
        """Save notebook content.
        
        Args:
            path: Notebook path
            content: Notebook content
            format: Content format (default: 'json')
            
        Returns:
            Updated Contents object
        """
        data = {
            "type": "notebook", 
            "format": format,
            "content": content,
        }
        
        encoded_path = quote(path, safe="/")
        response = self.http_client.put(f"/api/contents/{encoded_path}", json_data=data)
        return Contents(**response)
    
    def save_file(
        self,
        path: str,
        content: str,
        format: str = "text",
    ) -> Contents:
        """Save file content.
        
        Args:
            path: File path
            content: File content
            format: Content format ('text', 'base64')
            
        Returns:
            Updated Contents object
        """
        data = {
            "type": "file",
            "format": format, 
            "content": content,
        }
        
        encoded_path = quote(path, safe="/")
        response = self.http_client.put(f"/api/contents/{encoded_path}", json_data=data)
        return Contents(**response)
    
    def rename(self, old_path: str, new_path: str) -> Contents:
        """Rename a file or directory.
        
        Args:
            old_path: Current path
            new_path: New path
            
        Returns:
            Updated Contents object
        """
        data = {"path": new_path}
        
        encoded_path = quote(old_path, safe="/")
        response = self.http_client.patch(f"/api/contents/{encoded_path}", json_data=data)
        return Contents(**response)
    
    def copy_file(self, from_path: str, to_path: str) -> Contents:
        """Copy a file.
        
        Args:
            from_path: Source file path
            to_path: Destination path
            
        Returns:
            Contents object for copied file
        """
        # First, copy to a temporary location
        copy_data = {"copy_from": from_path}
        
        # Get directory and filename from to_path
        import os
        directory = os.path.dirname(to_path)
        
        encoded_dir = quote(directory, safe="/") if directory else ""
        response = self.http_client.post(f"/api/contents/{encoded_dir}", json_data=copy_data)
        
        # Then rename if needed
        temp_file = Contents(**response)
        if temp_file.path != to_path:
            return self.rename(temp_file.path, to_path)
        
        return temp_file
    
    def delete(self, path: str) -> None:
        """Delete a file or directory.
        
        Args:
            path: Path to delete
        """
        encoded_path = quote(path, safe="/")
        self.http_client.delete(f"/api/contents/{encoded_path}")
    
    def create_untitled(
        self,
        path: str = "",
        type: str = "notebook",
        ext: Optional[str] = None,
    ) -> Contents:
        """Create an untitled file/notebook.
        
        Args:
            path: Directory path (default: root)
            type: Content type ('notebook', 'file', 'directory')
            ext: File extension (for files)
            
        Returns:
            Contents object for created item
        """
        data = {"type": type}
        if ext:
            data["ext"] = ext
        
        encoded_path = quote(path, safe="/") if path else ""
        response = self.http_client.post(f"/api/contents/{encoded_path}", json_data=data)
        return Contents(**response)
    
    # Checkpoints methods
    def list_checkpoints(self, path: str) -> List[Dict[str, Any]]:
        """List checkpoints for a file.
        
        Args:
            path: File path
            
        Returns:
            List of checkpoint information
        """
        encoded_path = quote(path, safe="/")
        return self.http_client.get(f"/api/contents/{encoded_path}/checkpoints")
    
    def create_checkpoint(self, path: str) -> Dict[str, Any]:
        """Create a checkpoint for a file.
        
        Args:
            path: File path
            
        Returns:
            Checkpoint information
        """
        encoded_path = quote(path, safe="/")
        return self.http_client.post(f"/api/contents/{encoded_path}/checkpoints")
    
    def restore_checkpoint(self, path: str, checkpoint_id: str) -> None:
        """Restore a file to a checkpoint.
        
        Args:
            path: File path
            checkpoint_id: Checkpoint ID
        """
        encoded_path = quote(path, safe="/")
        self.http_client.post(f"/api/contents/{encoded_path}/checkpoints/{checkpoint_id}")
    
    def delete_checkpoint(self, path: str, checkpoint_id: str) -> None:
        """Delete a checkpoint.
        
        Args:
            path: File path
            checkpoint_id: Checkpoint ID
        """
        encoded_path = quote(path, safe="/")
        self.http_client.delete(f"/api/contents/{encoded_path}/checkpoints/{checkpoint_id}")
