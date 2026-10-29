"""Schemas of the invoice categorization and of the advice."""

from typing import Literal

from pydantic import BaseModel, Field

InvoiceCategory = Literal[
    "alimentacao",
    "transporte",
    "moradia",
    "saude",
    "educacao",
    "lazer",
    "compras",
    "assinaturas",
    "servicos",
    "juros_e_taxas",
    "outros",
]


class TransactionCategory(BaseModel):
    """Category chosen for one transaction of the invoice."""

    index: int = Field(
        description="Position of the transaction in the list sent to the model."
    )
    category: InvoiceCategory = Field(
        description="Category selected from the allowed labels."
    )


class TransactionCategories(BaseModel):
    """Categories chosen for the transactions of an invoice."""

    categories: list[TransactionCategory] = Field(
        description="One item per transaction, using the transaction index."
    )


class Suggestion(BaseModel):
    """One concrete suggestion to reduce the cost of the card."""

    title: str = Field(description="Short title of the suggestion.")
    detail: str = Field(
        description="Explanation based only on the numbers of the invoice."
    )
    estimated_monthly_saving: float | None = Field(
        description=(
            "Estimated monthly saving in BRL computed from the numbers, "
            "or null if it cannot be estimated."
        ),
    )


class InvoiceAdvice(BaseModel):
    """Summary of the invoice and up to three suggestions."""

    summary: str = Field(
        description="Two or three sentences describing where the money went."
    )
    suggestions: list[Suggestion] = Field(
        description="Up to three concrete suggestions; empty if there is nothing to suggest."
    )
