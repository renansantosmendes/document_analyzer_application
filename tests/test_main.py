"""Tests of the application factory."""

from fastapi.testclient import TestClient

from document_analyzer.main import create_app


def test_create_app_registers_the_health_and_upload_routes():
    paths = create_app().openapi()["paths"]
    assert "/health" in paths
    assert "/upload" in paths


def test_cors_allows_the_page_opened_from_disk_to_call_the_api():
    with TestClient(create_app()) as client:
        response = client.options(
            "/upload",
            headers={
                "Origin": "null",
                "Access-Control-Request-Method": "POST",
            },
        )
    assert response.headers["access-control-allow-origin"] == "*"
