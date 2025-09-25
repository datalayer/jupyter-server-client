# Copyright (c) 2025 Datalayer, Inc.
#
# BSD 3-Clause License

"""Sessions API manager for session operations."""

from typing import Any, Dict, List, Optional, Union

from jupyter_server_client.models import Session


class SessionsManager:
    """Manager for Sessions API operations."""
    
    def __init__(self, http_client: Any):
        """Initialize sessions manager.
        
        Args:
            http_client: HTTP client instance
        """
        self.http_client = http_client
    
    def list_sessions(self) -> List[Session]:
        """List all active sessions.
        
        Returns:
            List of Session objects
        """
        response = self.http_client.get("/api/sessions")
        return [Session(**session) for session in response]
    
    def get_session(self, session_id: str) -> Session:
        """Get information about a specific session.
        
        Args:
            session_id: Session UUID
            
        Returns:
            Session object
        """
        response = self.http_client.get(f"/api/sessions/{session_id}")
        return Session(**response)
    
    def create_session(
        self,
        path: str,
        kernel: Union[Dict[str, Any], None] = None,
        session_type: str = "notebook",
        name: Optional[str] = None,
    ) -> Session:
        """Create a new session.
        
        Args:
            path: Path to the notebook/file
            kernel: Kernel specification or object
            session_type: Type of session ('notebook', 'file', etc.)
            name: Session name
            
        Returns:
            Session object for created session
        """
        data = {
            "path": path,
            "type": session_type,
        }
        
        if name:
            data["name"] = name
        
        if kernel:
            # Assume kernel is a dictionary with kernel info
            data["kernel"] = kernel
        
        response = self.http_client.post("/api/sessions", json_data=data)
        return Session(**response)
    
    def update_session(
        self,
        session_id: str,
        path: Optional[str] = None,
        name: Optional[str] = None,
        session_type: Optional[str] = None,
        kernel: Optional[Dict[str, Any]] = None,
    ) -> Session:
        """Update an existing session.
        
        Args:
            session_id: Session UUID
            path: New path for the session
            name: New session name
            session_type: New session type
            kernel: New kernel specification
            
        Returns:
            Updated Session object
        """
        data: Dict[str, Any] = {}
        
        if path is not None:
            data["path"] = path
        if name is not None:
            data["name"] = name
        if session_type is not None:
            data["type"] = session_type
        if kernel is not None:
            # Assume kernel is a dictionary with kernel info
            data["kernel"] = kernel
        
        response = self.http_client.patch(f"/api/sessions/{session_id}", json_data=data)
        return Session(**response)
    
    def delete_session(self, session_id: str) -> None:
        """Delete a session.
        
        Args:
            session_id: Session UUID
        """
        self.http_client.delete(f"/api/sessions/{session_id}")
    
    def rename_session(self, session_id: str, new_path: str) -> Session:
        """Rename a session (change its path).
        
        Args:
            session_id: Session UUID
            new_path: New path for the session
            
        Returns:
            Updated Session object
        """
        return self.update_session(session_id, path=new_path)
