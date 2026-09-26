from __future__ import annotations

import pytest

from participium.services.auth_service import AuthService

from participium.models.user import User
from participium.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ValidationError,
)

EXISTING_USER = User(
    id=1,
    username="tom.hanks",
    first_name="Tom",
    last_name="Hanks",
    email="forrest.gump@example.com",
    password_hash="VALID_HASH",
    is_active=True,
    is_email_verified=True,
)

INACTIVE_USER = User(
    id=2,
    username="inactive.user",
    first_name="Inactive",
    last_name="User",
    email="inactive.user@example.com",
    password_hash="VALID_HASH_INACTIVE",
    is_active=False,
    is_email_verified=True,
)

VALID_PASSWORD = "correct_password"
INVALID_PASSWORD = "wrong_password"

# AUTH-01
@pytest.mark.skip(reason="Disabled.")
def test_authenticate_valid_username_correct_password() -> None:
    auth_service = AuthService()

    result = auth_service.authenticate(
        identifier=EXISTING_USER.username,
        password=VALID_PASSWORD,
    )

    assert isinstance(result, User)
    assert result.id == EXISTING_USER.id
    assert result.username == EXISTING_USER.username
    assert result.email == EXISTING_USER.email


# AUTH-02
@pytest.mark.skip(reason="Disabled.")
def test_authenticate_valid_email_correct_password() -> None:
    auth_service = AuthService()

    result = auth_service.authenticate(
        identifier=EXISTING_USER.email,
        password=VALID_PASSWORD,
    )

    assert isinstance(result, User)
    assert result.id == EXISTING_USER.id

# AUTH-03
@pytest.mark.skip(reason="Disabled.")
def test_authenticate_valid_username_invalid_password() -> None:
    auth_service = AuthService()

    with pytest.raises(AuthenticationError):
        auth_service.authenticate(
            identifier=EXISTING_USER.username,
            password=INVALID_PASSWORD,
        )

# AUTH-04
@pytest.mark.skip(reason="Disabled.")
def test_authenticate_valid_email_invalid_password() -> None:
    auth_service = AuthService()

    with pytest.raises(AuthenticationError):
        auth_service.authenticate(
            identifier=EXISTING_USER.email,
            password=INVALID_PASSWORD,
        )

# AUTH-05
@pytest.mark.skip(reason="Disabled.")
def test_authenticate_invalid_username() -> None:
    auth_service = AuthService()

    with pytest.raises(AuthenticationError):
        auth_service.authenticate(
            identifier="unknown.user",
            password=VALID_PASSWORD,
        )

# AUTH-06
@pytest.mark.skip(reason="Disabled.")
def test_authenticate_invalid_email() -> None:
    auth_service = AuthService()

    with pytest.raises(AuthenticationError):
        auth_service.authenticate(
            identifier="unknown@email.com",
            password=VALID_PASSWORD,
        )

# AUTH-07
@pytest.mark.skip(reason="Disabled.")
def test_authenticate_empty_identifier() -> None:
    auth_service = AuthService()

    with pytest.raises(ValidationError):
        auth_service.authenticate(
            identifier="",
            password=VALID_PASSWORD,
        )

# AUTH-08
@pytest.mark.skip(reason="Disabled.")
def test_authenticate_valid_username_empty_password() -> None:
    auth_service = AuthService()

    with pytest.raises(ValidationError):
        auth_service.authenticate(
            identifier=EXISTING_USER.username,
            password="",
        )

# AUTH-09
@pytest.mark.skip(reason="Disabled.")
def test_authenticate_valid_email_empty_password() -> None:
    auth_service = AuthService()

    with pytest.raises(ValidationError):
        auth_service.authenticate(
            identifier=EXISTING_USER.email,
            password="",
        )

# AUTH-10
@pytest.mark.skip(reason="Disabled.")
def test_authenticate_empty_identifier_and_password() -> None:
    auth_service = AuthService()

    with pytest.raises(ValidationError):
        auth_service.authenticate(
            identifier="",
            password="",
        )

# AUTH-11
@pytest.mark.skip(reason="Disabled.")
def test_authenticate_inactive_user() -> None:
    auth_service = AuthService()

    with pytest.raises(AuthorizationError):
        auth_service.authenticate(
            identifier=INACTIVE_USER.username,
            password=VALID_PASSWORD,
        )






