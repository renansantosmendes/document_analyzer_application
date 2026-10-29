"""Analysis pipeline: classify a document, then extract the fields of its category."""

from typing import Any

from document_analyzer.classification.classifier import classify_document
from document_analyzer.extraction.extractor import extract_fields
from document_analyzer.invoice_analysis.analyzer import analyze_invoice

INVOICE_TYPE = "credit_card_invoice"


def extract_document(llm: Any, file_name: str, text: str) -> dict[str, Any]:
    """Classify a document, then extract the fields of its category.

    For a credit card invoice, the transactions are also analysed: the result
    ``data`` gets an ``analysis`` entry with the totals and the advice.

    Parameters
    ----------
    llm : Any
        Chat model that supports ``with_structured_output``.
    file_name : str
        Name of the uploaded file, given to the model as context.
    text : str
        Text extracted from the PDF.

    Returns
    -------
    dict[str, Any]
        ``document_type`` and ``justification`` of the classification, and
        ``data`` with the extracted fields (``None`` for unsupported types).
    """
    classification = classify_document(llm, file_name, text)
    data = extract_fields(llm, classification.document_type, file_name, text)
    if classification.document_type == INVOICE_TYPE and data is not None:
        data["analysis"] = analyze_invoice(llm, data["transactions"])
    return {
        "document_type": classification.document_type,
        "justification": classification.justification,
        "data": data,
    }
