"""Tests of the invoice analysis with a fake model (no network)."""

from document_analyzer.classification.schemas import DocumentClassification
from document_analyzer.invoice_analysis.analyzer import analyze_invoice
from document_analyzer.invoice_analysis.schemas import (
    InvoiceAdvice,
    Suggestion,
    TransactionCategories,
    TransactionCategory,
)
from tests.helpers import FakeStructuredLLM

TRANSACTIONS = [
    {"date": "05/01", "description": "Supermercado", "amount": 300.0, "installment": None},
    {"date": "07/01", "description": "Netflix", "amount": 55.9, "installment": None},
    {"date": "09/01", "description": "Multa de atraso", "amount": 20.0, "installment": None},
]


def fake_llm():
    return FakeStructuredLLM(
        DocumentClassification(document_type="other", justification="x"),
        {
            TransactionCategories: TransactionCategories(categories=[
                TransactionCategory(index=0, category="alimentacao"),
                TransactionCategory(index=1, category="assinaturas"),
                TransactionCategory(index=2, category="juros_e_taxas"),
            ]),
            InvoiceAdvice: InvoiceAdvice(
                summary="Alimentação lidera os gastos.",
                suggestions=[Suggestion(title="Pague em dia", detail="Evite a multa.", estimated_monthly_saving=20.0)],
            ),
        },
    )


def test_the_categories_of_the_model_are_used_for_the_totals():
    result = analyze_invoice(fake_llm(), TRANSACTIONS)
    labels = {item["category"]: item["total"] for item in result["by_category"]}
    assert labels == {"alimentacao": 300.0, "assinaturas": 55.9, "juros_e_taxas": 20.0}
    assert result["total_spent"] == 375.9
    assert result["financial_costs"] == 20.0


def test_the_advice_comes_with_the_summary_and_the_suggestions():
    result = analyze_invoice(fake_llm(), TRANSACTIONS)
    assert result["advice"]["summary"] == "Alimentação lidera os gastos."
    assert result["advice"]["suggestions"][0]["title"] == "Pague em dia"


def test_the_model_receives_the_totals_as_json_for_the_advice():
    llm = fake_llm()
    analyze_invoice(llm, TRANSACTIONS)
    assert any('"total_spent": 375.9' in prompt for prompt in llm.prompts)


def test_an_invoice_without_charges_skips_the_model():
    llm = fake_llm()
    result = analyze_invoice(llm, [{"date": None, "description": "Pagamento", "amount": -50.0, "installment": None}])
    assert result["total_spent"] == 0.0
    assert result["advice"]["suggestions"] == []
    assert llm.prompts == []
