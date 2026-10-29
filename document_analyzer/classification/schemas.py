"""Schema of the document classification."""

from typing import Literal

from pydantic import BaseModel, Field

DocumentType = Literal[
    "service_contract",
    "lease_contract",
    "extrajudicial_notice",
    "power_of_attorney",
    "nda",
    "other",
]


class DocumentClassification(BaseModel):
    """Predicted document category and a brief evidence-based rationale."""

    document_type: DocumentType = Field(
        description="Document category selected from the allowed labels."
    )
    justification: str = Field(
        description="Brief justification based on the document text."
    )
