from __future__ import annotations

import pytest

from participium.core.exceptions import ValidationError
from participium.services.user_service import UserService
from participium.models.user import User
from werkzeug.datastructures import FileStorage

ADMIN_USER = User(
    id=105,
    username="ajeje.brazorf",
    first_name="Aldo",
    last_name="Baglio",
    role="admin",
    is_active=True,
    email_notifications_enabled=True,
    category_id=1
)

OPERATOR_USER = User(
    id=106,
    username="fausto.gervasoni",
    first_name="Giacomino",
    last_name="Poretti",
    role="operator",
    is_active=True,
    email_notifications_enabled=True,
    category_id=2
)

CITIZEN_USER = User(
    id=107,
    username="ignazio.ilsurname",
    first_name="Giovanni",
    last_name="Storti",
    role="citizen",
    is_active=True,
    category_id=2
)

photo_storage = FileStorage(filename="profile_pic.jpg", content_type="image/jpeg", content_length=1024)

# USERNAME ALREADY USED BY ANOTHER ACCOUNT
@pytest.mark.skip(reason="Disabled.")
def test_verify_username_already_used() -> None:
    user_service = UserService()

    with pytest.raises(ValidationError):
        user_service.update_profile(user=CITIZEN_USER, username=OPERATOR_USER.username)


# CORRECT PARTIAL UPDATE (ONLY SOME FIELDS)
@pytest.mark.skip(reason="Disabled.")
def test_verify_update_profile_partial_success() -> None:
    user_service = UserService()

    # Aggiorniamo solo first_name e disabilitiamo le notifiche, lasciando gli altri a None
    updated_user = user_service.update_profile(user=OPERATOR_USER, first_name="Guglielmo", email_notifications_enabled=False)
    
    assert updated_user.first_name == "Guglielmo"
    assert updated_user.email_notifications_enabled is False
    # check that the other fields have remained unchanged
    assert updated_user.username == "fausto.gervasoni"
    assert updated_user.last_name == "Poretti"
    assert updated_user.role == "operator"
    assert updated_user.is_active == True
    assert updated_user.category_id == 2


# CORRECT FULL UPDATE (ALL FIELDS)
@pytest.mark.skip(reason="Disabled.")
def test_verify_update_profile_full_success() -> None:
    user_service = UserService()

    updated_user = user_service.update_profile(user=ADMIN_USER, username="rolando.ilfenomeno", first_name="Rolando", last_name="Nullazzo", email_notifications_enabled=False, profile_picture=photo_storage)
    
    assert updated_user.username == "rolando.ilfenomeno"
    assert updated_user.first_name == "Rolando"
    assert updated_user.last_name == "Nullazzo"
    assert updated_user.email_notifications_enabled is False
    assert updated_user.profile_picture == photo_storage
    assert updated_user.category_id == 1
    assert updated_user.is_active == True
