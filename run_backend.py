#!/usr/bin/env python3
"""
Run script for SoundMatchBot backend.
Handles virtual environment activation and proper imports.
"""

import sys
import os
import subprocess

def main():
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Warning: Not running in a virtual environment.")
        print("Consider creating one: python3 -m venv venv && source venv/bin/activate")
        print("Continuing anyway...\n")

    # Check if config.yaml exists
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if not os.path.exists(config_path):
        print("Error: config.yaml not found in project root.")
        print("Please create config.yaml based on the README instructions.")
        sys.exit(1)

    # Check if we're in the right directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    if not os.path.exists(backend_dir):
        print("Error: backend directory not found.")
        print("Make sure you're running from the project root.")
        sys.exit(1)

    # Ensure we run uvicorn from the project root so "backend" is importable as a package
    project_root = os.path.abspath(os.path.dirname(__file__))

    # Run uvicorn pointing to the package module
    venv_python = os.path.join(project_root, '.venv', 'bin', 'python')
    cmd = [venv_python, '-m', 'uvicorn', 'backend.main:app', '--reload', '--host', '0.0.0.0', '--port', '8000']
    print(f"Starting server with command: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, cwd=project_root)
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()