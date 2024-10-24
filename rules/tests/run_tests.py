#!/usr/bin/env python3
import unittest
import sys
import os

def setup_django_environment():
    # Add the parent directory (rule_engine) to Python path
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # Add the current app directory to Python path
    app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if app_root not in sys.path:
        sys.path.insert(0, app_root)

def run_tests():
    """Run all test files in the tests directory"""
    # Setup the environment
    setup_django_environment()
    
    # Initialize the test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Discover and add all tests
    test_suite = loader.discover(
        current_dir,
        pattern='*_test*.py',
        top_level_dir=os.path.dirname(os.path.dirname(current_dir))
    )
    suite.addTests(test_suite)
    
    # Run the tests
    runner = unittest.TextTestRunner(
        verbosity=2,
        failfast=False,
        buffer=True,
        descriptions=True
    )
    
    result = runner.run(suite)
    
    # Print summary
    print("\nTest Summary:")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())