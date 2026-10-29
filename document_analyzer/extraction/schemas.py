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
        description="Whether authority to settle/transigir is expressly granted, or null if unclear."
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
