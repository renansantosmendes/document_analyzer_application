"""Totals of an invoice grouped by category and by merchant (pure functions)."""

from collections import defaultdict
from typing import Any

CATEGORY_LABELS = {
    "alimentacao": "Alimentação",
    "transporte": "Transporte",
    "moradia": "Moradia",
    "saude": "Saúde",
    "educacao": "Educação",
    "lazer": "Lazer",
    "compras": "Compras",
    "assinaturas": "Assinaturas",
    "servicos": "Serviços",
    "juros_e_taxas": "Juros e taxas",
    "outros": "Outros",
}
TOP_MERCHANTS = 5
FEES_CATEGORY = "juros_e_taxas"


def summarize_invoice(
    transactions: list[dict[str, Any]],
    categories: dict[int, str],
) -> dict[str, Any]:
    """Group the charges of an invoice by category and by merchant.

    Only positive amounts (charges and fees) count as spending; payments and
    credits are reported apart. A transaction without a category falls into
    "outros".

    Parameters
    ----------
    transactions : list[dict[str, Any]]
        Transactions as extracted, each with ``description`` and ``amount``.
    categories : dict[int, str]
        Category of each transaction, by its position in the list.

    Returns
    -------
    dict[str, Any]
        ``total_spent``, ``transaction_count``, ``credits_total``,
        ``financial_costs``, ``by_category`` (sorted by total, with share and
        count), and ``top_merchants``.

    Example
    -------
    >>> transactions = [{"description": "Padaria", "amount": 10.0}]
    >>> summarize_invoice(transactions, {0: "alimentacao"})["total_spent"]
    10.0
    """
    by_category: dict[str, dict[str, float]] = defaultdict(lambda: {"total": 0.0, "count": 0})
    merchants: dict[str, float] = defaultdict(float)
    credits_total = 0.0
    spent_total = 0.0
    charge_count = 0

    for index, transaction in enumerate(transactions):
        amount = float(transaction["amount"])
        if amount <= 0:
            credits_total += -amount
            continue
        category = categories.get(index, "outros")
        spent_total += amount
        charge_count += 1
        by_category[category]["total"] += amount
        by_category[category]["count"] += 1
        merchants[transaction["description"].strip().upper()] += amount

    ordered = sorted(by_category.items(), key=lambda item: item[1]["total"], reverse=True)
    ranked_merchants = sorted(
        merchants.items(), key=lambda item: item[1], reverse=True
    )[:TOP_MERCHANTS]
    share = {
        name: round(values["total"] / spent_total * 100, 1) if spent_total else 0.0
        for name, values in ordered
    }
    return {
        "total_spent": round(spent_total, 2),
        "transaction_count": charge_count,
        "credits_total": round(credits_total, 2),
        "financial_costs": round(by_category.get(FEES_CATEGORY, {"total": 0.0})["total"], 2),
        "by_category": [
            {
                "category": name,
                "label": CATEGORY_LABELS.get(name, name),
                "total": round(values["total"], 2),
                "count": values["count"],
                "share_percent": share[name],
            }
            for name, values in ordered
        ],
        "top_merchants": [
            {"description": name, "total": round(total, 2)}
            for name, total in ranked_merchants
        ],
    }
