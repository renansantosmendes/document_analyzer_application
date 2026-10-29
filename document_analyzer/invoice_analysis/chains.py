"""Chains of the invoice analysis: categorize the transactions and advise."""

import json
from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from document_analyzer.invoice_analysis.schemas import InvoiceAdvice, TransactionCategories

CATEGORIZATION_INSTRUCTION = (
    "Você classifica lançamentos de fatura de cartão de crédito brasileira. "
    "Escolha para cada lançamento uma categoria: alimentacao, transporte, "
    "moradia, saude, educacao, lazer, compras, assinaturas, servicos, "
    "juros_e_taxas (juros, multas, IOF, anuidade e encargos) ou outros. "
    "Responda um item por lançamento, usando o índice informado. Baseie-se "
    "somente na descrição."
)

ADVICE_INSTRUCTION = (
    "Você é um consultor financeiro para pessoas físicas. Com base somente nos "
    "números do resumo da fatura, descreva onde o dinheiro foi gasto e sugira "
    "até três melhorias concretas para reduzir custos com o cartão, como "
    "parcelamento, juros, assinaturas e concentração em uma categoria. Não "
    "invente valores, use os números informados para estimar economias e não "
    "recomende produtos financeiros específicos."
)

CATEGORIZATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", CATEGORIZATION_INSTRUCTION),
    ("human", "Lançamentos (índice | data | descrição | valor em reais):\n{transactions}"),
])

ADVICE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", ADVICE_INSTRUCTION),
    ("human", "Resumo da fatura em JSON:\n{summary}"),
])


def build_categorization_chain(llm: Any) -> Runnable:
    """Create the chain that assigns a category to each transaction.

    Parameters
    ----------
    llm : Any
        Chat model that supports ``with_structured_output``.

    Returns
    -------
    Runnable
        Chain that receives ``transactions`` as text and returns
        ``TransactionCategories``.
    """
    return CATEGORIZATION_PROMPT | llm.with_structured_output(TransactionCategories)


def build_advice_chain(llm: Any) -> Runnable:
    """Create the chain that writes the summary and the suggestions.

    Parameters
    ----------
    llm : Any
        Chat model that supports ``with_structured_output``.

    Returns
    -------
    Runnable
        Chain that receives ``summary`` as JSON text and returns ``InvoiceAdvice``.
    """
    return ADVICE_PROMPT | llm.with_structured_output(InvoiceAdvice)


def categorize_transactions(llm: Any, transactions: list[dict[str, Any]]) -> dict[int, str]:
    """Ask the model for the category of each transaction.

    Parameters
    ----------
    llm : Any
        Chat model that supports ``with_structured_output``.
    transactions : list[dict[str, Any]]
        Transactions as extracted from the invoice.

    Returns
    -------
    dict[int, str]
        Category of each transaction index that the model answered.
    """
    lines = "\n".join(
        f"{index} | {item.get('date') or '-'} | {item['description']} | {item['amount']}"
        for index, item in enumerate(transactions)
    )
    result = build_categorization_chain(llm).invoke({"transactions": lines})
    return {item.index: item.category for item in result.categories}


def advise(llm: Any, summary: dict[str, Any]) -> InvoiceAdvice:
    """Write the summary and the suggestions from the computed totals.

    Parameters
    ----------
    llm : Any
        Chat model that supports ``with_structured_output``.
    summary : dict[str, Any]
        Totals computed by ``summarize_invoice``.

    Returns
    -------
    InvoiceAdvice
        Summary of the invoice and the suggestions.
    """
    return build_advice_chain(llm).invoke(
        {"summary": json.dumps(summary, ensure_ascii=False, indent=2)}
    )
