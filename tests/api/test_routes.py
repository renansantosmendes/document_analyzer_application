"""Tests of the health route and the upload route."""

from fastapi.testclient import TestClient

from document_analyzer.api import routes
from document_analyzer.main import create_app


def test_health_reports_ok():
    with TestClient(create_app()) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_returns_the_classification_and_the_extracted_fields(monkeypatch):
    monkeypatch.setattr(routes, "get_token", lambda: "fake-token")
    monkeypatch.setattr(routes, "extract_text_from_pdf", lambda content: "texto do pdf")
    monkeypatch.setattr(
        routes,
        "extract_document",
        lambda llm, file_name, text: {
            "document_type": "nda",
            "justification": "Acordo de confidencialidade.",
            "data": {"party_a_name": "A"},
        },
    )
    with TestClient(create_app()) as client:
        response = client.post(
            "/upload",
            files={"file": ("acordo.pdf", b"%PDF-1.4 conteudo", "application/pdf")},
        )
    assert response.status_code == 200
    assert response.json()["document_type"] == "nda"
    assert response.json()["data"] == {"party_a_name": "A"}


def test_upload_refuses_a_file_that_is_not_a_readable_pdf(monkeypatch):
    monkeypatch.setattr(routes, "get_token", lambda: "fake-token")
    with TestClient(create_app()) as client:
        response = client.post(
            "/upload",
            files={"file": ("nota.txt", b"isto nao e um pdf", "text/plain")},
        )
    assert response.status_code == 422
    assert response.json()["detail"] == "The file is not a readable PDF."


def test_upload_refuses_a_pdf_without_selectable_text(monkeypatch):
    monkeypatch.setattr(routes, "get_token", lambda: "fake-token")
    monkeypatch.setattr(routes, "extract_text_from_pdf", lambda content: "")
    with TestClient(create_app()) as client:
        response = client.post(
            "/upload",
            files={"file": ("digitalizado.pdf", b"%PDF-1.4 conteudo", "application/pdf")},
        )
    assert response.status_code == 422
    assert response.json()["detail"] == "The PDF has no selectable text."


def test_upload_without_a_file_is_refused_by_validation():
    with TestClient(create_app()) as client:
        assert client.post("/upload").status_code == 422


def test_upload_explains_a_missing_credential(monkeypatch):
    def missing_credentials():
        raise KeyError("PGL_PASSWORD")

    monkeypatch.setattr(routes, "get_token", missing_credentials)
    with TestClient(create_app()) as client:
        response = client.post(
            "/upload",
            files={"file": ("nota.pdf", b"%PDF-1.4 conteudo", "application/pdf")},
        )
    assert response.status_code == 500
    assert "PGL_PASSWORD" in response.json()["detail"]
