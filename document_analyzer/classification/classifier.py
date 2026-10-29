"""Classification chain: decides the category of a legal document."""

from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from document_analyzer.classification.schemas import DocumentClassification
from document_analyzer.llm.client import truncate_text

CLASSIFICATION_INSTRUCTION = (
    "Classifique documentos jurídicos brasileiros usando exatamente uma "
    "categoria: service_contract (contrato de prestação de serviços), "
    "lease_contract (contrato de locação), extrajudicial_notice "
    "(notificação extrajudicial), power_of_attorney (procuração), nda "
    "(acordo de confidencialidade) ou other (outro documento). Baseie-se "
    "somente no texto. Não extraia ainda os campos do documento e não invente "
    "informações."
)

CLASSIFICATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", CLASSIFICATION_INSTRUCTION),
    ("human", "Nome do arquivo: {file_name}\nTexto do documento:\n{text}"),
])


def build_classification_chain(llm: Any) -> Runnable:
    """Create the chain that classifies a document into one category.

    Parameters
    ----------
    llm : Any
        Chat model that supports ``with_structured_output``.

    Returns
    -------
    Runnable
        Chain that receives ``file_name`` and ``text`` and returns a
        ``DocumentClassification``.
    """
    return CLASSIFICATION_PROMPT | llm.with_structured_output(
        DocumentClassification
    )


def classify_document(llm: Any, file_name: str, text: str) -> DocumentClassification:
    """Classify the text of a document.

    Parameters
    ----------
    llm : Any
        Chat model that supports ``with_structured_output``.
    file_name : str
        Name of the uploaded file, given to the model as context.
    text : str
        Text extracted from the PDF; only the part allowed by ``truncate_text``
        is sent to the model.

    Returns
    -------
    DocumentClassification
        Category and justification chosen by the model.
    """
    return build_classification_chain(llm).invoke(
        {"file_name": file_name, "text": truncate_text(text)}
    )
