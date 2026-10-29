"""Tests of the shared auth client and of the token lookup."""

import pytest

from document_analyzer.auth import client as auth_client


@pytest.fixture
def fresh_auth_client():
    """Clear the shared auth client before and after a test.

    Yields
    ------
    None
        Nothing; the cache is cleared around the test.
    """
    auth_client.get_auth_client.cache_clear()
    yield
    auth_client.get_auth_client.cache_clear()


class RecordingAuthClient:
    """Stand-in of ``PGLAuthClient`` that records the logins it receives."""

    logins = []

    def __init__(self) -> None:
        self.token = None

    def login(self, registration_number, password):
        """Record the credentials and keep a fixed token.

        Parameters
        ----------
        registration_number : str
            Registration number used to log in.
        password : str
            Password used to log in.

        Returns
        -------
        str
            Fixed token.
        """
        RecordingAuthClient.logins.append((registration_number, password))
        self.token = "fake-token"
        return self.token


def test_get_token_logs_in_once_and_reuses_the_client(monkeypatch, fresh_auth_client):
    RecordingAuthClient.logins = []
    monkeypatch.setattr(auth_client, "PGLAuthClient", RecordingAuthClient)
    monkeypatch.setenv("PGL_REGISTRATION_NUMBER", "2024001")
    monkeypatch.setenv("PGL_PASSWORD", "segredo")
    assert auth_client.get_token() == "fake-token"
    assert auth_client.get_token() == "fake-token"
    assert RecordingAuthClient.logins == [("2024001", "segredo")]


def test_get_token_refuses_to_log_in_without_credentials(monkeypatch, fresh_auth_client):
    monkeypatch.setattr(auth_client, "PGLAuthClient", RecordingAuthClient)
    monkeypatch.delenv("PGL_REGISTRATION_NUMBER", raising=False)
    monkeypatch.delenv("PGL_PASSWORD", raising=False)
    with pytest.raises(KeyError):
        auth_client.get_token()
