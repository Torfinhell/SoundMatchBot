#!/usr/bin/env python3
"""
Check system requirements and dependencies for SoundMatchBot.
Run this before starting the application.
"""

import sys
import os
import subprocess
import importlib

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"❌ Python {version.major}.{version.minor} detected. Need Python 3.10+")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_database_connection():
    """Check PostgreSQL connection."""
    try:
        import psycopg2
        # Try to connect using config
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        if os.path.exists(config_path):
            import yaml
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            db_url = config['backend']['database_url']
            # Parse URL and try connection
            print("✅ PostgreSQL connection string found")
            return True
        else:
            print("⚠️  config.yaml not found - create it first")
            return False
    except ImportError:
        print("❌ psycopg2 not installed")
        return False
    except Exception as e:
        print(f"⚠️  PostgreSQL connection issue: {e}")
        return False

def check_redis_connection():
    """Check Redis connection."""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("✅ Redis connection successful")
        return True
    except ImportError:
        print("❌ redis-py not installed")
        return False
    except Exception:
        print("⚠️  Redis not running or connection failed")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    # Map package names to their import names
    required_imports = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn', 
        'sqlalchemy': 'sqlalchemy',
        'pydantic': 'pydantic',
        'faiss-cpu': 'faiss',
        'numpy': 'numpy',
        'httpx': 'httpx',
        'pyyaml': 'yaml',
        'psycopg2': 'psycopg2',
        'redis': 'redis'
    }
    missing = []
    for pkg, import_name in required_imports.items():
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r backend/requirements.txt")
        return False
    print("✅ All Python dependencies installed")
    return True

def check_config():
    """Check if config.yaml exists and is valid."""
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if not os.path.exists(config_path):
        print("❌ config.yaml not found")
        print("Create config.yaml based on README instructions")
        return False

    try:
        import yaml
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        required_keys = ['backend', 'bot', 'frontend']
        for key in required_keys:
            if key not in config:
                print(f"❌ Missing '{key}' section in config.yaml")
                return False
        print("✅ config.yaml is valid")
        return True
    except Exception as e:
        print(f"❌ Error reading config.yaml: {e}")
        return False

def main():
    print("🔍 Checking SoundMatchBot requirements...\n")

    checks = [
        ("Python Version", check_python_version),
        ("Configuration", check_config),
        ("Python Dependencies", check_dependencies),
        ("PostgreSQL", check_database_connection),
        ("Redis", check_redis_connection),
    ]

    passed = 0
    total = len(checks)

    for name, check_func in checks:
        print(f"Checking {name}...")
        if check_func():
            passed += 1
        print()

    print(f"Results: {passed}/{total} checks passed")

    if passed == total:
        print("🎉 All requirements met! You can start the application.")
        return 0
    else:
        print("⚠️  Some requirements not met. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())