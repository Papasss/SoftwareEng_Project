from __future__ import annotations

import pytest

from participium.core.security import verify_password

CORRECT_PASSWORD = "correct_password"
INCORRECT_PASSWORD = "wrong_password"
EMPTY_PASSWORD = ""

VALID_HASH = "valid_hash"
INVALID_HASH = "invalid_hash"

# PSW-01
@pytest.mark.skip(reason="Disabled.")
def test_verify_password_correct_password_valid_hash() -> None:
    result = verify_password(
        password=CORRECT_PASSWORD,
        password_hash=VALID_HASH,
    )

    assert result is True

# PSW-02
@pytest.mark.skip(reason="Disabled.")
def test_verify_password_incorrect_password_valid_hash() -> None:
    result = verify_password(
        password=INCORRECT_PASSWORD,
        password_hash=VALID_HASH,
    )

    assert result is False

# PSW-03
@pytest.mark.skip(reason="Disabled.")
def test_verify_password_empty_password_valid_hash() -> None:
    result = verify_password(
        password=EMPTY_PASSWORD,
        password_hash=VALID_HASH,
    )

    assert result is False

# PSW-04
@pytest.mark.skip(reason="Disabled.")
def test_verify_password_correct_password_invalid_hash() -> None:
    result = verify_password(
        password=CORRECT_PASSWORD,
        password_hash=INVALID_HASH,
    )

    assert result is False

# PSW-05
@pytest.mark.skip(reason="Disabled.")
def test_verify_password_incorrect_password_invalid_hash() -> None:
    result = verify_password(
        password=INCORRECT_PASSWORD,
        password_hash=INVALID_HASH,
    )

    assert result is False

# PSW-06
@pytest.mark.skip(reason="Disabled.")
def test_verify_password_empty_password_invalid_hash() -> None:
    result = verify_password(
        password=EMPTY_PASSWORD,
        password_hash=INVALID_HASH,
    )

    assert result is False