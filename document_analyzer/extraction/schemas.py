"""Schemas of the fields extracted from each category of document."""

from pydantic import BaseModel, Field


class ServiceContractData(BaseModel):
    """Fields extracted from a service provision contract."""

    contractor_name: str | None = Field(
        description="Contracting party, or null if absent."
    )
    provider_name: str | None = Field(
        description="Service provider, or null if absent."
    )
    contract_value: float | None = Field(
        description="Total contract value in BRL, or null if absent."
    )
    number_of_installments: int | None = Field(
        description="Number of installments, or null if absent."
    )
    termination_penalty_pct: float | None = Field(
        description="Early termination penalty percentage, or null if absent."
    )
    auto_renewal: bool | None = Field(
        description="Whether automatic renewal is expressly provided, or null if unclear."
    )
    forum: str | None = Field(
        description="Elected jurisdiction/forum, or null if absent."
    )


class LeaseContractData(BaseModel):
    """Fields extracted from a commercial lease contract."""

    landlord_name: str | None = Field(
        description="Landlord name, or null if absent."
    )
    tenant_name: str | None = Field(
        description="Tenant name, or null if absent."
    )
    monthly_rent: float | None = Field(
        description="Monthly rent in BRL, or null if absent."
    )
    guarantee_amount: float | None = Field(
        description="Rental guarantee amount in BRL, or null if absent."
    )
    term_months: int | None = Field(
        description="Lease duration in months, or null if absent."
    )


class ExtrajudicialNoticeData(BaseModel):
    """Fields extracted from an extrajudicial notice."""

    notifying_party: str | None = Field(
        description="Party sending the notice, or null if absent."
    )
    notified_party: str | None = Field(
        description="Party receiving the notice, or null if absent."
    )
    lawyer_name: str | None = Field(
        description="Signing lawyer, or null if absent."
    )
    lawyer_oab: str | None = Field(
        description="Lawyer's OAB registration, or null if absent."
    )
    installment_values: list[float] = Field(
        description="Explicitly stated overdue installment values in BRL; empty if absent."
    )
    total_amount: float | None = Field(
        description="Total amount claimed in BRL, or null if absent."
    )
    response_deadline_days: int | None = Field(
        description="Deadline in days, or null if absent."
    )


class PowerOfAttorneyData(BaseModel):
    """Fields extracted from a power of attorney."""

    grantor_name: str | None = Field(
        description="Grantor name, or null if absent."
    )
    lawyer_registrations: list[str] = Field(
        description="OAB registrations of appointed lawyers; empty if absent."
    )
    counterparty_name: str | None = Field(
        description="Opposing party name, or null if absent."
    )
    counterparty_cnpj: str | None = Field(
        description="Opposing party CNPJ, or null if absent."
    )
    allows_settlement: bool | None = Field(
        description=(
            "Whether authority to settle/transigir is expressly granted, "
            "or null if unclear."
        ),
    )


class NdaData(BaseModel):
    """Fields extracted from a non-disclosure agreement."""

    party_a_name: str | None = Field(
        description="First party name, or null if absent."
    )
    party_a_cnpj: str | None = Field(
        description="First party CNPJ, or null if absent."
    )
    party_b_name: str | None = Field(
        description="Second party name, or null if absent."
    )
    party_b_cnpj: str | None = Field(
        description="Second party CNPJ, or null if absent."
    )
    penalty_amount: float | None = Field(
        description="Confidentiality breach penalty in BRL, or null if absent."
    )
    term_years: int | None = Field(
        description="Confidentiality term in years, or null if absent."
    )


class InvoiceTransaction(BaseModel):
    """One charge or payment listed in a credit card invoice."""

    date: str | None = Field(
        description="Transaction date as written in the invoice, or null if absent."
    )
    description: str = Field(
        description="Merchant or description exactly as written in the invoice."
    )
    amount: float = Field(
        description="Amount in BRL: positive for charges, negative for payments and credits."
    )
    installment: str | None = Field(
        description="Installment information such as '3/10', or null if not in installments."
    )


class CreditCardInvoiceData(BaseModel):
    """Fields extracted from a credit card invoice."""

    issuer_bank: str | None = Field(
        description="Card issuer or bank name, or null if absent."
    )
    cardholder_name: str | None = Field(
        description="Cardholder name, or null if absent."
    )
    card_last_digits: str | None = Field(
        description="Last four digits of the card, or null if absent."
    )
    closing_date: str | None = Field(
        description="Invoice closing date as written, or null if absent."
    )
    due_date: str | None = Field(
        description="Payment due date as written, or null if absent."
    )
    total_amount: float | None = Field(
        description="Total amount of the invoice in BRL, or null if absent."
    )
    minimum_payment: float | None = Field(
        description="Minimum payment in BRL, or null if absent."
    )
    interest_and_fees: float | None = Field(
        description=(
            "Interest, fines and fees charged in this invoice in BRL, "
            "or null if none are stated."
        ),
    )
    transactions: list[InvoiceTransaction] = Field(
        description="Every transaction listed in the invoice, in order; empty if absent."
    )
