"""Chat model of the PGL proxy and the limit of text sent to it."""

from langchain_openai import ChatOpenAI

PROXY_BASE_URL = "https://pgl-proxy.vercel.app/v1"
MODEL_NAME = "gpt-4o-mini"
MAX_TEXT_CHARS = 60_000


def build_llm(api_key: str) -> ChatOpenAI:
    """Build the chat model that calls the PGL proxy.

    Parameters
    ----------
    api_key : str
        Access token of the auth service, accepted by the proxy.

    Returns
    -------
    ChatOpenAI
        Chat model configured for the proxy.
    """
    return ChatOpenAI(base_url=PROXY_BASE_URL, api_key=api_key, model=MODEL_NAME)


def truncate_text(text: str) -> str:
    """Cut a document text to the number of characters the model receives.

    Parameters
    ----------
    text : str
        Text extracted from the document.

    Returns
    -------
    str
        The first ``MAX_TEXT_CHARS`` characters of the text.
    """
    return text[:MAX_TEXT_CHARS]
