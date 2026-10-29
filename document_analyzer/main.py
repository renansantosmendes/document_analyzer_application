"""FastAPI application: creates the app and includes the routes."""

from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_openai import ChatOpenAI

from document_analyzer.api.routes import router

load_dotenv()


def create_app() -> FastAPI:
    """Build the FastAPI application with its routes.

    Returns
    -------
    FastAPI
        Application with the health and upload routes.

    Example
    -------
    >>> from fastapi.testclient import TestClient
    >>> client = TestClient(create_app())
    >>> client.get("/health").json()
    {'status': 'ok'}
    """
    app = FastAPI(title="Document Analyzer", version="0.1.0")
    app.include_router(router)
    return app


app = create_app()

if __name__ == "__main__":
    from uvicorn import run
    run("document_analyzer.main:app", host="127.0.0.1", port=8000)
