"""Full analysis of an invoice: categories, totals, chart data and advice."""

from typing import Any

from document_analyzer.invoice_analysis.chains import advise, categorize_transactions
from document_analyzer.invoice_analysis.summary import summarize_invoice


def analyze_invoice(llm: Any, transactions: list[dict[str, Any]]) -> dict[str, Any]:
    """Analyse the transactions of an invoice.

    The model only categorizes the transactions and writes the advice; every
    total is computed in Python. An invoice without charges skips the model.

    Parameters
    ----------
    llm : Any
        Chat model that supports ``with_structured_output``.
    transactions : list[dict[str, Any]]
        Transactions as extracted from the invoice.

    Returns
    -------
    dict[str, Any]
        Totals and groupings from ``summarize_invoice`` plus ``advice``, with
        ``summary`` and ``suggestions``.
    """
    if not any(float(item["amount"]) > 0 for item in transactions):
        summary = summarize_invoice(transactions, {})
        advice = {"summary": "Nenhum gasto encontrado na fatura.", "suggestions": []}
        return {**summary, "advice": advice}
    categories = categorize_transactions(llm, transactions)
    summary = summarize_invoice(transactions, categories)
    advice = advise(llm, summary)
    return {**summary, "advice": advice.model_dump()}
