"""Tests of the chat model configuration and of the text limit."""

from document_analyzer.llm import client


def test_the_model_talks_to_the_pgl_proxy_with_the_given_token():
    llm = client.build_llm("token-de-teste")
    assert llm.openai_api_base == client.PROXY_BASE_URL
    assert llm.model_name == client.MODEL_NAME


def test_truncate_text_keeps_only_the_allowed_characters(monkeypatch):
    monkeypatch.setattr(client, "MAX_TEXT_CHARS", 4)
    assert client.truncate_text("abcdefgh") == "abcd"
    assert client.truncate_text("ab") == "ab"
