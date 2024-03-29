"""Example entry point."""

from __future__ import annotations

from src.app import make_app

if __name__ == "__main__":
    import sys

    sys.exit("python -m uvicorn src.main:app --port 8080 --reload")


app = make_app()
