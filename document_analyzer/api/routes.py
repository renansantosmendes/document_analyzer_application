"""HTTP routes: health check and PDF upload with classification and extraction."""

from typing import Any

from fastapi import APIRouter, File, HTTPException, UploadFile
from pypdf.errors import PdfReadError

from document_analyzer.analysis.pipeline import extract_document
from document_analyzer.auth.client import get_token
from document_analyzer.llm.client import build_llm
from document_analyzer.pdf.text import extract_text_from_pdf

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """Report that the service is running.

    Returns
    -------
    dict[str, str]
        Status of the service.
    """
    return {"status": "ok"}


@router.post("/upload")
def upload(file: UploadFile = File(...)) -> dict[str, Any]:
    """Receive a PDF, classify it and extract the fields of its category.

    The auth service is called before the file is read. The token it returns
    is the key of the LLM proxy.

    Parameters
    ----------
    file : UploadFile
        PDF file sent as multipart form data under the field ``file``.

    Returns
    -------
    dict[str, Any]
        ``document_type``, ``justification`` and ``data`` (the extracted fields,
        or ``None`` for a category without an extractor).

    Raises
    ------
    HTTPException
        With status 422 when the file is not a readable PDF or has no
        selectable text.
    """
    token = get_token()
    try:
        text = extract_text_from_pdf(file.file.read())
    except (PdfReadError, ValueError) as error:
        raise HTTPException(
            status_code=422,
            detail="The file is not a readable PDF.",
        ) from error
    if not text:
        raise HTTPException(
            status_code=422,
            detail="The PDF has no selectable text.",
        )
    return extract_document(build_llm(token), file.filename or "documento.pdf", text)
