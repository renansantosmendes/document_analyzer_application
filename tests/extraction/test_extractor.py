"""Tests of the extraction chains, with a fake model (no network)."""

from document_analyzer.classification.schemas import DocumentClassification
from document_analyzer.extraction.extractor import extract_fields
from document_analyzer.extraction.schemas import NdaData, ServiceContractData
from tests.helpers import FakeStructuredLLM


def test_nda_fields_are_extracted_with_the_nda_schema():
    llm = FakeStructuredLLM(
        DocumentClassification(document_type="nda", justification="x"),
        {NdaData: NdaData(
            party_a_name="Acme", party_a_cnpj=None, party_b_name="Beta",
            party_b_cnpj=None, penalty_amount=50000.0, term_years=2,
        )},
    )
    fields = extract_fields(llm, "nda", "acordo.pdf", "Texto do acordo")
    assert fields["party_a_name"] == "Acme"
    assert fields["penalty_amount"] == 50000.0


def test_service_contract_fields_are_extracted_with_their_schema():
    llm = FakeStructuredLLM(
        DocumentClassification(document_type="service_contract", justification="x"),
        {ServiceContractData: ServiceContractData(
            contractor_name="Cliente", provider_name="Prestador", contract_value=1200.0,
            number_of_installments=12, termination_penalty_pct=10.0, auto_renewal=True,
            forum="São Paulo",
        )},
    )
    fields = extract_fields(llm, "service_contract", "servico.pdf", "Texto")
    assert fields["contract_value"] == 1200.0
    assert fields["auto_renewal"] is True


def test_a_category_without_extractor_returns_none():
    llm = FakeStructuredLLM(
        DocumentClassification(document_type="other", justification="x"),
        {},
    )
    assert extract_fields(llm, "other", "outro.pdf", "Texto") is None
