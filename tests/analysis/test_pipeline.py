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


def test_an_invoice_is_classified_extracted_and_analysed():
    from document_analyzer.extraction.schemas import CreditCardInvoiceData, InvoiceTransaction
    from document_analyzer.invoice_analysis.schemas import InvoiceAdvice, TransactionCategories, TransactionCategory

    invoice = CreditCardInvoiceData(
        issuer_bank="Banco X", cardholder_name=None, card_last_digits=None,
        closing_date=None, due_date=None, total_amount=120.0, minimum_payment=None,
        interest_and_fees=None,
        transactions=[InvoiceTransaction(date="02/01", description="Farmácia", amount=120.0, installment=None)],
    )
    llm = FakeStructuredLLM(
        DocumentClassification(document_type="credit_card_invoice", justification="Fatura."),
        {
            CreditCardInvoiceData: invoice,
            TransactionCategories: TransactionCategories(
                categories=[TransactionCategory(index=0, category="saude")]
            ),
            InvoiceAdvice: InvoiceAdvice(summary="Saúde.", suggestions=[]),
        },
    )
    result = extract_document(llm, "fatura.pdf", "Texto da fatura")
    assert result["document_type"] == "credit_card_invoice"
    assert result["data"]["issuer_bank"] == "Banco X"
    assert result["data"]["analysis"]["by_category"][0]["category"] == "saude"
    assert result["data"]["analysis"]["advice"]["summary"] == "Saúde."
