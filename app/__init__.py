"""FastAPI application package.

This file marks the `app` directory as a Python package. It doesn't need
to contain any logic but allows importing the application via
`app.main:app` for uvicorn and for tests.
"""

# Expose the FastAPI app at package level for convenience
from .main import app as app

__all__ = ["app"]
