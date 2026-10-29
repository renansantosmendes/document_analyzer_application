"""Tests of the extraction schemas: nullable fields and type coercion."""

from document_analyzer.extraction.schemas import ExtrajudicialNoticeData, NdaData, ServiceContractData


def test_optional_fields_accept_null_when_the_text_has_no_value():
    data = ServiceContractData(
        contractor_name=None,
        provider_name="Acme Ltda",
        contract_value=None,
        number_of_installments=None,
        termination_penalty_pct=None,
        auto_renewal=None,
        forum=None,
    )
    assert data.contractor_name is None
    assert data.provider_name == "Acme Ltda"


def test_extracted_values_are_coerced_to_their_types():
    data = NdaData(
        party_a_name="A",
        party_a_cnpj=None,
        party_b_name="B",
        party_b_cnpj=None,
        penalty_amount="10000.5",
        term_years="5",
    )
    assert data.penalty_amount == 10000.5
    assert data.term_years == 5


def test_list_fields_keep_the_values_stated_in_the_notice():
    data = ExtrajudicialNoticeData(
        notifying_party="Credor",
        notified_party="Devedor",
        lawyer_name=None,
        lawyer_oab=None,
        installment_values=[1200.0, 1200.0],
        total_amount=2400.0,
        response_deadline_days=15,
    )
    assert data.installment_values == [1200.0, 1200.0]
