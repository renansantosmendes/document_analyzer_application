"""Tests of the classification chain, with a fake model (no network)."""

import pytest
from pydantic import ValidationError

from document_analyzer.classification.classifier import classify_document
from document_analyzer.classification.schemas import DocumentClassification
from document_analyzer.llm import client
from tests.helpers import FakeStructuredLLM


def test_the_document_is_classified_with_its_justification():
    llm = FakeStructuredLLM(
        DocumentClassification(document_type="nda", justification="Sigilo."),
        {},
    )
    result = classify_document(llm, "acordo.pdf", "Texto do acordo")
    assert result.document_type == "nda"
    assert result.justification == "Sigilo."


def test_the_text_sent_to_the_model_is_truncated(monkeypatch):
    monkeypatch.setattr(client, "MAX_TEXT_CHARS", 5)
    llm = FakeStructuredLLM(
        DocumentClassification(document_type="other", justification="x"),
        {},
    )
    classify_document(llm, "a.pdf", "abcdefgh")
    assert "Texto do documento:\nabcde" in llm.prompts[0]
    assert "abcdef" not in llm.prompts[0]


def test_a_label_outside_the_allowed_list_is_refused():
    with pytest.raises(ValidationError):
        DocumentClassification(document_type="invoice", justification="x")
