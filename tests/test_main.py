"""Tests of the application factory."""

from document_analyzer.main import create_app


def test_create_app_registers_the_health_and_upload_routes():
    paths = create_app().openapi()["paths"]
    assert "/health" in paths
    assert "/upload" in paths
