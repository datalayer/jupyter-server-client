#!/usr/bin/env python3
"""Example usage of the ExecsManager for synchronous kernel execution.

This demonstrates the undocumented /api/kernels/{kernel_id}/execute endpoint.
"""

from jupyter_server_api import JupyterServerClient

# Configuration
BASE_URL = "http://localhost:8888"
TOKEN = "MY_TOKEN"  # Replace with your token

def main():
    # Create client
    client = JupyterServerClient(base_url=BASE_URL, token=TOKEN)
    
    try:
        # Step 1: Get list of running kernels (or start a session to create one)
        print("Fetching running kernels...")
        kernels = client.kernels.list_kernels()
        
        if not kernels:
            print("No running kernels found. Please start a kernel first.")
            print("You can start a session using:")
            print("  client.sessions.create_session(name='test', path='test.ipynb', type='notebook')")
            return
        
        # Use the first available kernel
        kernel = kernels[0]
        print(f"Using kernel: {kernel.id} ({kernel.name})")
        
        # Step 2: Execute simple code
        print("\n--- Executing: print('Hello, World!') ---")
        result = client.execs.execute(kernel.id, "print('Hello, World!')")
        print(f"Status: {result.status}")
        print(f"Execution count: {result.execution_count}")
        print(f"Outputs: {result.parsed_outputs}")
        
        # Step 3: Execute code with a return value
        print("\n--- Executing: 1 + 1 ---")
        result = client.execs.execute(kernel.id, "1 + 1")
        print(f"Status: {result.status}")
        print(f"Execution count: {result.execution_count}")
        print(f"Outputs: {result.parsed_outputs}")
        
        # Step 4: Execute code that creates variables
        print("\n--- Executing: x = 42; y = x * 2; print(f'x={x}, y={y}') ---")
        result = client.execs.execute(
            kernel.id,
            "x = 42\ny = x * 2\nprint(f'x={x}, y={y}')"
        )
        print(f"Status: {result.status}")
        print(f"Execution count: {result.execution_count}")
        print(f"Outputs: {result.parsed_outputs}")
        
        # Step 5: Execute code that causes an error
        print("\n--- Executing: 1 / 0 (will error) ---")
        try:
            result = client.execs.execute(kernel.id, "1 / 0")
            print(f"Status: {result.status}")
            print(f"Execution count: {result.execution_count}")
            print(f"Outputs: {result.parsed_outputs}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Step 6: Execute code with matplotlib (if available)
        print("\n--- Executing: matplotlib plot ---")
        plot_code = """
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y)
plt.title('Sine Wave')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.grid(True)
plt.show()

print('Plot generated!')
"""
        try:
            result = client.execs.execute(kernel.id, plot_code, timeout=10.0)
            print(f"Status: {result.status}")
            print(f"Execution count: {result.execution_count}")
            print(f"Number of outputs: {len(result.parsed_outputs)}")
            # Note: Image outputs will be base64-encoded PNG data
            for i, output in enumerate(result.parsed_outputs):
                print(f"Output {i}: {output.get('output_type', 'unknown')}")
        except Exception as e:
            print(f"Skipped (matplotlib not available or error): {e}")
        
    finally:
        # Clean up
        client.close()
        print("\nClient closed.")


if __name__ == "__main__":
    main()
