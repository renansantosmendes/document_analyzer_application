"""Tests of the PDF text extraction, with a blank PDF and a fake text layer."""

import io

from document_analyzer.pdf import text as pdf_text
from document_analyzer.pdf.text import extract_text_from_pdf
from tests.helpers import blank_pdf


class FakePage:
    """Page whose text layer is fixed.

    Parameters
    ----------
    text : str | None
        Text returned by ``extract_text``.
    """

    def __init__(self, text: str | None) -> None:
        self._text = text

    def extract_text(self) -> str | None:
        """Return the fixed text of the page.

        Returns
        -------
        str | None
            The text given to the constructor.
        """
        return self._text


class FakeReader:
    """Reader that exposes fixed pages instead of parsing a file.

    Parameters
    ----------
    stream : io.BytesIO
        Ignored; kept to match ``PdfReader``.
    """

    pages = [FakePage("Primeira página"), FakePage(None), FakePage("  Última  ")]

    def __init__(self, stream: io.BytesIO) -> None:
        self.stream = stream


def test_pages_are_joined_with_line_breaks_and_stripped(monkeypatch):
    monkeypatch.setattr(pdf_text, "PdfReader", FakeReader)
    assert extract_text_from_pdf(b"%PDF-1.4 fake") == "Primeira página\n\n  Última"


def test_a_blank_pdf_has_no_text():
    assert extract_text_from_pdf(blank_pdf(2)) == ""
