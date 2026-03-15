#!/usr/bin/env python3
"""
Initialize the database tables for SoundMatchBot.
Run from the backend directory: python -m scripts.init_db
"""

import sys
import os

# Change to backend directory
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(backend_dir)

# Add current directory to Python path
sys.path.insert(0, backend_dir)

try:
    from database import engine, Base
    from models import User, Poll, PollAnswer, UserEmbedding

    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running this from the backend directory:")
    print("  cd backend && python -m scripts.init_db")
    sys.exit(1)
except Exception as e:
    print(f"Error creating database tables: {e}")
    print("Make sure your database is running and the connection string in config.yaml is correct.")
    sys.exit(1)