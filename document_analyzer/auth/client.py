"""Authentication with the PGL auth service, shared by the routes."""

import os
from functools import lru_cache

from pgl_auth import PGLAuthClient


@lru_cache
def get_auth_client() -> PGLAuthClient:
    """Authentication client shared by every request of the process.

    Returns
    -------
    PGLAuthClient
        Client that keeps the token of the last login.
    """
    return PGLAuthClient()


def get_token() -> str:
    """Token of the auth service, logging in only when there is none.

    Returns
    -------
    str
        Access token of the auth service.

    Raises
    ------
    KeyError
        When ``PGL_REGISTRATION_NUMBER`` or ``PGL_PASSWORD`` is not set.
    """
    client = get_auth_client()
    if client.token is None:
        client.login(
            registration_number=os.environ["PGL_REGISTRATION_NUMBER"],
            password=os.environ["PGL_PASSWORD"],
        )
    return client.token
