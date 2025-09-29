#!/usr/bin/env python3
"""
Test runner script for jupyter-server-api.

This script runs all tests and provides a summary of the results.
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import jupyter_server_api
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def run_tests():
    """Run all tests and return the result."""
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('\\n')[-2]}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\\n')[-2]}")
    
    # Return success status
    return len(result.failures) == 0 and len(result.errors) == 0


def run_specific_test(test_name):
    """Run a specific test module or test case."""
    try:
        # Try to load and run the specific test
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromName(test_name)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return len(result.failures) == 0 and len(result.errors) == 0
    except Exception as e:
        print(f"Error running test {test_name}: {e}")
        return False


if __name__ == '__main__':
    print("🧪 Running jupyter-server-api tests...")
    print("=" * 70)
    
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        success = run_specific_test(test_name)
    else:
        # Run all tests
        success = run_tests()
    
    if success:
        print("\\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\\n❌ Some tests failed!")
        sys.exit(1)
