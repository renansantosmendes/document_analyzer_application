"""Tests of the analysis pipeline: classification followed by extraction."""

from document_analyzer.analysis.pipeline import extract_document
from document_analyzer.classification.schemas import DocumentClassification
from document_analyzer.extraction.schemas import NdaData
from tests.helpers import FakeStructuredLLM


def test_a_document_is_classified_and_its_fields_extracted():
    llm = FakeStructuredLLM(
        DocumentClassification(document_type="nda", justification="Sigilo."),
        {NdaData: NdaData(
            party_a_name="Acme", party_a_cnpj=None, party_b_name="Beta",
            party_b_cnpj=None, penalty_amount=50000.0, term_years=2,
        )},
    )
    result = extract_document(llm, "acordo.pdf", "Texto do acordo")
    assert result["document_type"] == "nda"
    assert result["justification"] == "Sigilo."
    assert result["data"]["party_a_name"] == "Acme"


def test_a_category_without_extractor_returns_no_data():
    llm = FakeStructuredLLM(
        DocumentClassification(document_type="other", justification="Outro tipo."),
        {},
    )
    result = extract_document(llm, "outro.pdf", "Texto qualquer")
    assert result["document_type"] == "other"
    assert result["data"] is None
