"""Text extraction from PDF files."""

import io

from pypdf import PdfReader


def extract_text_from_pdf(pdf_content: bytes) -> str:
    """Extract the text of all pages of a PDF.

    Pages without a text layer (scanned images, for example) contribute
    nothing, and the pages are joined with a line break.

    Parameters
    ----------
    pdf_content : bytes
        Raw bytes of the PDF file.

    Returns
    -------
    str
        Text of the document, without surrounding spaces.

    Example
    -------
    >>> with open("contrato.pdf", "rb") as file:  # doctest: +SKIP
    ...     text = extract_text_from_pdf(file.read())
    """
    reader = PdfReader(io.BytesIO(pdf_content))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages).strip()
