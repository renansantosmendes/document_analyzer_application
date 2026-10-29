"""Tests of the invoice totals: pure functions, no model involved."""

from document_analyzer.invoice_analysis.summary import summarize_invoice

TRANSACTIONS = [
    {"description": "Padaria Central", "amount": 40.0},
    {"description": "Uber", "amount": 25.5},
    {"description": "padaria central", "amount": 10.0},
    {"description": "Juros rotativo", "amount": 30.0},
    {"description": "Pagamento recebido", "amount": -200.0},
]
CATEGORIES = {0: "alimentacao", 1: "transporte", 2: "alimentacao", 3: "juros_e_taxas"}


def test_charges_are_totalled_and_payments_are_kept_apart():
    summary = summarize_invoice(TRANSACTIONS, CATEGORIES)
    assert summary["total_spent"] == 105.5
    assert summary["transaction_count"] == 4
    assert summary["credits_total"] == 200.0


def test_categories_are_sorted_by_total_with_share_and_label():
    by_category = summarize_invoice(TRANSACTIONS, CATEGORIES)["by_category"]
    assert [item["category"] for item in by_category] == ["alimentacao", "juros_e_taxas", "transporte"]
    food = by_category[0]
    assert food["total"] == 50.0
    assert food["count"] == 2
    assert food["label"] == "Alimentação"
    assert food["share_percent"] == 47.4


def test_financial_costs_are_the_fees_category():
    assert summarize_invoice(TRANSACTIONS, CATEGORIES)["financial_costs"] == 30.0


def test_without_fees_there_are_no_financial_costs_and_no_empty_fee_entry():
    summary = summarize_invoice(
        [{"description": "Mercado", "amount": 90.0}], {0: "alimentacao"}
    )
    assert summary["financial_costs"] == 0.0
    assert [item["category"] for item in summary["by_category"]] == ["alimentacao"]


def test_a_transaction_without_category_falls_into_outros():
    summary = summarize_invoice([{"description": "X", "amount": 12.0}], {})
    assert summary["by_category"][0]["category"] == "outros"


def test_merchants_are_grouped_ignoring_case_and_sorted_by_total():
    merchants = summarize_invoice(TRANSACTIONS, CATEGORIES)["top_merchants"]
    assert merchants[0] == {"description": "PADARIA CENTRAL", "total": 50.0}
    assert len(merchants) == 3


def test_an_invoice_without_charges_has_zero_totals():
    summary = summarize_invoice([{"description": "Pagamento", "amount": -10.0}], {})
    assert summary["total_spent"] == 0.0
    assert summary["by_category"] == []
    assert summary["credits_total"] == 10.0
