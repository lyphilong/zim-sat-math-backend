"""
Vercel entrypoint for FastAPI application
This file exports the FastAPI app so Vercel can detect it
"""
import sys
import os

# Add api directory to path so imports work correctly
# This allows us to import backend.main as backend.main
api_path = os.path.dirname(__file__)
if api_path not in sys.path:
    sys.path.insert(0, api_path)

# Import the FastAPI app from backend/main.py
from backend.main import app

# Export the app for Vercel
__all__ = ["app"]

