#!/usr/bin/env python3
"""
Example usage of jupyter-server-client library with Datalayer integration.

This script demonstrates how to use the server client alongside existing
jupyter-nbmodel-client and jupyter-kernel-client for comprehensive Jupyter operations.
Make sure you have a Jupyter Server running before executing this script.
"""

import os
import sys
from pathlib import Path

# Add the package to the path for testing
sys.path.insert(0, str(Path(__file__).parent))

from jupyter_server_client import JupyterServerClient, JupyterServerError


def main():
    """Demonstrate basic usage of the Jupyter Server client."""
    
    # Configuration - adjust these for your Jupyter Server
    base_url = os.getenv("JUPYTER_SERVER_URL", "http://localhost:8888")
    token = os.getenv("JUPYTER_TOKEN", "")
    
    print(f"Connecting to Jupyter Server at: {base_url}")
    
    try:
        # Create client
        with JupyterServerClient(base_url=base_url, token=token) as client:
            
            # Get server information
            print("\n1. Getting server version...")
            server_info = client.get_version()
            print(f"   Server version: {server_info.version}")
            
            # Get server status
            print("\n2. Getting server status...")
            status = client.get_status()
            print(f"   Status: {status}")
            
            # List available kernelspecs
            print("\n3. Listing available kernelspecs...")
            kernelspecs = client.kernelspecs.list_kernelspecs()
            print(f"   Available kernelspecs: {list(kernelspecs.kernelspecs.keys())}")
            
            # List contents in root directory
            print("\n4. Listing contents in root directory...")
            contents = client.contents.list_directory("")
            print(f"   Found {len(contents)} items:")
            for item in contents[:5]:  # Show first 5 items
                print(f"   - {item.name} ({item.type})")
            
            # Create a new notebook
            print("\n5. Creating a new notebook...")
            notebook_path = "example_notebook.ipynb"
            try:
                notebook = client.contents.create_notebook(notebook_path)
                print(f"   Created notebook: {notebook.name}")
                
                # Note: Kernel management is handled by jupyter-kernel-client
                print("\n6. Kernel management...")
                print("   Note: Use jupyter-kernel-client for kernel operations:")
                print("   from jupyter_kernel_client import KernelClient")
                print("   with KernelClient(server_url=..., token=...) as kernel:")
                print("       kernel.execute('print(\"Hello from kernel!\")')")
                
                # Create a session (without kernel for now)
                print("\n7. Creating a session...")
                session = client.sessions.create_session(notebook_path)
                print(f"   Created session: {session.id}")
                
                # List all sessions
                print("\n8. Listing all sessions...")
                sessions = client.sessions.list_sessions()
                print(f"   Total sessions: {len(sessions)}")
                
                # Clean up
                print("\n9. Cleaning up...")
                client.sessions.delete_session(session.id)
                print(f"    Deleted session: {session.id}")
                
                client.contents.delete(notebook_path)
                print(f"    Deleted notebook: {notebook_path}")
                
            except JupyterServerError as e:
                print(f"   Error creating notebook: {e}")
            
    except JupyterServerError as e:
        print(f"Error connecting to Jupyter Server: {e}")
        print("\nMake sure:")
        print("1. Jupyter Server is running")
        print("2. The URL is correct")
        print("3. The token is valid (if required)")
        return 1
    
    except ConnectionError as e:
        print(f"Connection error: {e}")
        return 1
    
    print("\nExample completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())
