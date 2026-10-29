"""Helpers shared by the tests: small PDFs and a fake structured model."""

import io

from langchain_core.runnables import RunnableLambda
from pypdf import PdfWriter

from document_analyzer.classification.schemas import DocumentClassification


def blank_pdf(pages: int) -> bytes:
    """Build a PDF with blank pages.

    Parameters
    ----------
    pages : int
        Number of blank pages to add.

    Returns
    -------
    bytes
        Raw bytes of the PDF.
    """
    writer = PdfWriter()
    for _index in range(pages):
        writer.add_blank_page(width=612, height=792)
    buffer = io.BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


class FakeStructuredLLM:
    """Model stand-in that answers with fixed objects per output schema.

    Parameters
    ----------
    classification : DocumentClassification
        Answer given when the classifier asks for the classification.
    answers : dict[type, object]
        Answer given for each extraction schema.
    """

    def __init__(
        self,
        classification: DocumentClassification,
        answers: dict,
    ) -> None:
        self.classification = classification
        self.answers = answers
        self.prompts = []

    def with_structured_output(self, schema):
        """Return a chain that answers with the fixed object of the schema.

        Parameters
        ----------
        schema : type
            Pydantic schema requested by the chain.

        Returns
        -------
        RunnableLambda
            Chain that records the prompt and returns the fixed answer.
        """

        def respond(prompt_value):
            self.prompts.append(prompt_value.to_messages()[-1].content)
            if schema is DocumentClassification:
                return self.classification
            return self.answers[schema]

        return RunnableLambda(respond)
