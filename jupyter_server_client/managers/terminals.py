# Copyright (c) 2025 Datalayer, Inc.
#
# BSD 3-Clause License

"""Terminals API manager for terminal operations."""

from typing import Any, List

from jupyter_server_client.models import Terminal


class TerminalsManager:
    """Manager for Terminals API operations."""
    
    def __init__(self, http_client: Any):
        """Initialize terminals manager.
        
        Args:
            http_client: HTTP client instance
        """
        self.http_client = http_client
    
    def list_terminals(self) -> List[Terminal]:
        """List all active terminals.
        
        Returns:
            List of Terminal objects
        """
        response = self.http_client.get("/api/terminals")
        return [Terminal(**terminal) for terminal in response]
    
    def get_terminal(self, terminal_name: str) -> Terminal:
        """Get information about a specific terminal.
        
        Args:
            terminal_name: Terminal name/ID
            
        Returns:
            Terminal object
        """
        response = self.http_client.get(f"/api/terminals/{terminal_name}")
        return Terminal(**response)
    
    def create_terminal(self) -> Terminal:
        """Create a new terminal.
        
        Returns:
            Terminal object for created terminal
        """
        response = self.http_client.post("/api/terminals")
        return Terminal(**response)
    
    def delete_terminal(self, terminal_name: str) -> None:
        """Delete a terminal.
        
        Args:
            terminal_name: Terminal name/ID
        """
        self.http_client.delete(f"/api/terminals/{terminal_name}")
    
    def shutdown_terminal(self, terminal_name: str) -> None:
        """Shutdown a terminal (alias for delete_terminal).
        
        Args:
            terminal_name: Terminal name/ID
        """
        self.delete_terminal(terminal_name)
