"""Extraction chains: one structured chain per category of document."""

from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from pydantic import BaseModel

from document_analyzer.extraction.schemas import (
    CreditCardInvoiceData,
    ExtrajudicialNoticeData,
    LeaseContractData,
    NdaData,
    PowerOfAttorneyData,
    ServiceContractData,
)
from document_analyzer.llm.client import truncate_text

EXTRACTION_RULES = (
    " Use somente informações explícitas no documento. Não infira nem invente "
    "dados. Se um campo não estiver disponível, use null ou uma lista vazia, "
    "conforme o schema."
)

EXTRACTION_SPECS = {
    "service_contract": (
        "Extraia os dados de um contrato de prestação de serviços. "
        "Valores monetários devem ser números em reais.",
        ServiceContractData,
    ),
    "lease_contract": (
        "Extraia os dados de um contrato de locação comercial. "
        "Valores monetários devem ser números em reais.",
        LeaseContractData,
    ),
    "extrajudicial_notice": (
        "Extraia os dados de uma notificação extrajudicial, incluindo valores "
        "em aberto e prazo de resposta.",
        ExtrajudicialNoticeData,
    ),
    "power_of_attorney": (
        "Extraia os dados de uma procuração, incluindo registros OAB e poderes "
        "para transigir.",
        PowerOfAttorneyData,
    ),
    "nda": (
        "Extraia os dados de um acordo de confidencialidade, incluindo partes, "
        "CNPJs, multa e prazo.",
        NdaData,
    ),
    "credit_card_invoice": (
        "Extraia os dados de uma fatura de cartão de crédito: banco emissor, "
        "titular, últimos dígitos, datas, total, pagamento mínimo, juros e "
        "encargos cobrados e todos os lançamentos, na ordem em que aparecem. "
        "Valores monetários devem ser números em reais; compras e encargos são "
        "positivos e pagamentos ou créditos são negativos.",
        CreditCardInvoiceData,
    ),
}


def build_extraction_chain(
    llm: Any,
    extraction_instruction: str,
    output_schema: type[BaseModel],
) -> Runnable:
    """Create a structured extraction chain for one document category.

    Parameters
    ----------
    llm : Any
        Chat model that supports ``with_structured_output``.
    extraction_instruction : str
        What to extract from this category of document.
    output_schema : type[BaseModel]
        Pydantic schema of the fields to extract.

    Returns
    -------
    Runnable
        Chain that receives ``file_name`` and ``text`` and returns the schema.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", extraction_instruction + EXTRACTION_RULES),
        ("human", "Arquivo: {file_name}\nDocumento:\n{text}"),
    ])
    return prompt | llm.with_structured_output(output_schema)


def extract_fields(
    llm: Any,
    document_type: str,
    file_name: str,
    text: str,
) -> dict[str, Any] | None:
    """Extract the fields of a classified document with its category's chain.

    Parameters
    ----------
    llm : Any
        Chat model that supports ``with_structured_output``.
    document_type : str
        Category returned by the classifier.
    file_name : str
        Name of the uploaded file, given to the model as context.
    text : str
        Text extracted from the PDF; only the part allowed by ``truncate_text``
        is sent to the model.

    Returns
    -------
    dict[str, Any] | None
        Extracted fields, or ``None`` when the category has no extractor.
    """
    if document_type not in EXTRACTION_SPECS:
        return None
    instruction, schema = EXTRACTION_SPECS[document_type]
    chain = build_extraction_chain(llm, instruction, schema)
    extracted = chain.invoke({"file_name": file_name, "text": truncate_text(text)})
    return extracted.model_dump()
