"""
Root FastAPI entrypoint for Vercel.

Vercel FastAPI integration (docs: https://vercel.com/docs/frameworks/backend/fastapi)
expects an `app` instance in app.py / index.py / server.py, etc.
We reuse the existing app defined in `api/backend/main.py`.
"""

from api.backend.main import app  # noqa: F401
