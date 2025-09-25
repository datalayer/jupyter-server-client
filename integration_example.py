#!/usr/bin/env python3
"""
Comprehensive example showing integration of all Datalayer Jupyter clients:
- jupyter-server-client: Server management + kernel listing (read-only)
- jupyter-kernel-client: Kernel management and code execution  
- jupyter-nbmodel-client: Real-time notebook collaboration

This demonstrates the full workflow from server setup to collaborative editing.
"""

import os
import sys
from pathlib import Path

# Add the package to the path for testing
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Demonstrate integration of all Datalayer Jupyter clients."""
    
    # Configuration
    base_url = os.getenv("JUPYTER_SERVER_URL", "http://localhost:8888")
    token = os.getenv("JUPYTER_TOKEN", "")
    
    print("🪐 Datalayer Jupyter Clients Integration Example")
    print("=" * 50)
    print(f"Server: {base_url}")
    
    try:
        # 1. SERVER MANAGEMENT (jupyter-server-client)
        print("\n📊 1. SERVER MANAGEMENT (jupyter-server-client)")
        print("-" * 45)
        
        from jupyter_server_client import JupyterServerClient
        
        with JupyterServerClient(base_url=base_url, token=token) as server:
            # Server status
            server_info = server.get_version() 
            print(f"✓ Server version: {server_info.version}")
            
            # List available kernelspecs
            kernelspecs = server.kernelspecs.list_kernelspecs()
            print(f"✓ Available kernelspecs: {list(kernelspecs.kernelspecs.keys())}")
            
            # Create notebook
            notebook_path = "integration_example.ipynb"
            notebook = server.contents.create_notebook(notebook_path)
            print(f"✓ Created notebook: {notebook.name}")
            
            # Create session
            session = server.sessions.create_session(notebook_path)
            print(f"✓ Created session: {session.id}")
            
            # NEW: List running kernels (read-only)
            print("\n� Kernel Listing:")
            kernels = server.kernels.list_kernels()
            print(f"✓ Found {len(kernels)} running kernels")
            for kernel in kernels:
                print(f"   - {kernel.id}: {kernel.name} ({kernel.execution_state})")
        
        # 2. INDIVIDUAL KERNEL INTERACTION (jupyter-kernel-client) 
        print("\n⚡ 2. INDIVIDUAL KERNEL INTERACTION (jupyter-kernel-client)")
        print("-" * 55)
        
        try:
            from jupyter_kernel_client import KernelClient
            
            with KernelClient(server_url=base_url, token=token) as kernel:
                print(f"✓ Started kernel: {kernel.id}")
                
                # Execute code
                result = kernel.execute("print('Hello from kernel!')")
                print(f"✓ Executed code, status: {result['status']}")
                
                # Another execution
                result = kernel.execute("x = 42; print(f'The answer is {x}')")
                print(f"✓ Set variable and printed, outputs: {len(result['outputs'])}")
                
        except ImportError:
            print("⚠️  jupyter-kernel-client not installed")
            print("   Install with: pip install jupyter-kernel-client")
        
        # 3. NOTEBOOK COLLABORATION (jupyter-nbmodel-client)
        print("\n📝 3. NOTEBOOK COLLABORATION (jupyter-nbmodel-client)")  
        print("-" * 45)
        
        try:
            from jupyter_nbmodel_client import NbModelClient, get_jupyter_notebook_websocket_url
            from jupyter_kernel_client import KernelClient
            
            # Get WebSocket URL for real-time collaboration
            ws_url = get_jupyter_notebook_websocket_url(
                server_url=base_url,
                token=token,
                path=notebook_path
            )
            
            # Collaborate on notebook
            with KernelClient(server_url=base_url, token=token) as kernel:
                async def collaborate():
                    async with NbModelClient(ws_url) as notebook:
                        # Add cells
                        cell_index = notebook.add_code_cell("print('Hello from collaborative notebook!')")
                        print(f"✓ Added code cell at index {cell_index}")
                        
                        # Execute cell
                        results = notebook.execute_cell(cell_index, kernel)
                        print(f"✓ Executed cell, status: {results['status']}")
                        
                        # Add markdown cell
                        md_index = notebook.add_markdown_cell("# Integration Success! 🎉")
                        print(f"✓ Added markdown cell at index {md_index}")
                        
                        print(f"✓ Notebook has {len(notebook)} cells")
                
                import asyncio
                asyncio.run(collaborate())
                
        except ImportError:
            print("⚠️  jupyter-nbmodel-client not installed") 
            print("   Install with: pip install jupyter-nbmodel-client")
        
        # 4. CLEANUP
        print("\n🧹 4. CLEANUP")
        print("-" * 15)
        
        with JupyterServerClient(base_url=base_url, token=token) as server:
            # Clean up session and notebook
            sessions = server.sessions.list_sessions()
            for session in sessions:
                if session.path == notebook_path:
                    server.sessions.delete_session(session.id)
                    print(f"✓ Deleted session: {session.id}")
            
            server.contents.delete(notebook_path)
            print(f"✓ Deleted notebook: {notebook_path}")
        
        print(f"\n🎊 Integration example completed successfully!")
        print("\nThis demonstrates how the three libraries work together:")
        print("• jupyter-server-client: Server and content management") 
        print("• jupyter-kernel-client: Kernel operations and execution")
        print("• jupyter-nbmodel-client: Real-time collaborative editing")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("1. Jupyter Server is running")
        print("2. The URL is correct") 
        print("3. The token is valid (if required)")
        print("4. Required packages are installed:")
        print("   pip install jupyter-server-client jupyter-kernel-client jupyter-nbmodel-client")
        return 1


if __name__ == "__main__":
    exit(main())
