from unittest.mock import Mock
from io import BytesIO

import pytest
from werkzeug.datastructures import FileStorage

from participium.services.user_service import UserService
from participium.models.user import User
from participium.models.enums import Role
from participium.core.exceptions import (
    NotFoundError,
    ValidationError,
)
from participium.core.security import hash_password


# Create a test user
def make_user(
    id=1,
    username="user",
    role=Role.CITIZEN,
):
    user = User(
        username=username,
        first_name="Test",
        last_name="User",
        email=f"{username}@test.com",
        password_hash=hash_password("secret"),
        role=role,
    )

    user.id = id

    return user


# Create fake uploaded image
def make_photo(filename="avatar.jpg"):
    return FileStorage(
        stream=BytesIO(b"fake-image"),
        filename=filename,
        content_type="image/jpeg",
    )


# Build service with mocked dependencies
def build_service():
    return UserService(
        session=Mock(),
        user_repository=Mock(),
        category_repository=Mock(),
        token_repository=Mock(),
        notification_repository=Mock(),
        storage_service=Mock(),
    )


# list_users should return repository result
def test_list_users():
    service = build_service()

    users = [make_user(id=1), make_user(id=2)]

    service.user_repository.list_all.return_value = users

    result = service.list_users()

    assert result == users


# get_user should return existing user
def test_get_user_success():
    service = build_service()

    user = make_user()

    service.user_repository.get_by_id.return_value = user

    result = service.get_user(1)

    assert result == user


# get_user should raise for missing user
def test_get_user_not_found():
    service = build_service()

    service.user_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        service.get_user(999)


# update_profile should update username
def test_update_profile_username():
    service = build_service()

    user = make_user()

    service.user_repository.get_by_username.return_value = None

    result = service.update_profile(
        user,
        username="newuser",
    )

    assert result.username == "newuser"

    service.session.commit.assert_called_once()


# update_profile should reject duplicate username
def test_update_profile_duplicate_username():
    service = build_service()

    user = make_user()

    service.user_repository.get_by_username.return_value = make_user(
        id=2,
        username="taken",
    )

    with pytest.raises(ValidationError):
        service.update_profile(
            user,
            username="taken",
        )


# update_profile should save profile picture
def test_update_profile_picture():
    service = build_service()

    user = make_user()

    service.storage_service.save.return_value = "saved-avatar.jpg"

    result = service.update_profile(
        user,
        profile_picture=make_photo(),
    )

    assert result.profile_picture_path == "saved-avatar.jpg"

    service.storage_service.save.assert_called_once()
    service.session.commit.assert_called_once()


# parse_role should return valid role
def test_parse_role_success():
    role = UserService._parse_role(
        Role.ADMIN.value,
    )

    assert role == Role.ADMIN


# parse_role should reject invalid role
def test_parse_role_invalid():
    with pytest.raises(ValidationError):
        UserService._parse_role(
            "INVALID_ROLE",
        )

# create_user should reject missing required fields
def test_create_user_missing_fields():
    service = build_service()

    with pytest.raises(ValidationError):
        service.create_user({})

# create_user should reject duplicate username
def test_create_user_duplicate_username():
    service = build_service()

    service.user_repository.get_by_username.return_value = object()

    payload = {
        "username": "user",
        "first_name": "Test",
        "last_name": "User",
        "email": "user@test.com",
        "password": "secret",
        "role": Role.CITIZEN.value,
    }

    with pytest.raises(ValidationError):
        service.create_user(payload)

# create_user should reject duplicate email
def test_create_user_duplicate_email():
    service = build_service()

    service.user_repository.get_by_username.return_value = None
    service.user_repository.get_by_email.return_value = object()

    payload = {
        "username": "user",
        "first_name": "Test",
        "last_name": "User",
        "email": "user@test.com",
        "password": "secret",
        "role": Role.CITIZEN.value,
    }

    with pytest.raises(ValidationError):
        service.create_user(payload)

# create_user should create citizen successfully
def test_create_user_success():
    service = build_service()

    service.user_repository.get_by_username.return_value = None
    service.user_repository.get_by_email.return_value = None

    payload = {
        "username": "newuser",
        "first_name": "Test",
        "last_name": "User",
        "email": "user@test.com",
        "password": "secret",
        "role": Role.CITIZEN.value,
    }

    result = service.create_user(payload)

    assert result.username == "newuser"

    service.user_repository.add.assert_called_once()
    service.session.commit.assert_called_once()

# operator must have category
def test_create_user_operator_requires_category():
    service = build_service()

    service.user_repository.get_by_username.return_value = None
    service.user_repository.get_by_email.return_value = None

    payload = {
        "username": "operator",
        "first_name": "Test",
        "last_name": "User",
        "email": "operator@test.com",
        "password": "secret",
        "role": Role.OPERATOR.value,
    }

    with pytest.raises(ValidationError):
        service.create_user(payload)

# operator category must exist
def test_create_user_operator_invalid_category():
    service = build_service()

    service.user_repository.get_by_username.return_value = None
    service.user_repository.get_by_email.return_value = None

    service.category_repository.get_by_id.return_value = None

    payload = {
        "username": "operator",
        "first_name": "Test",
        "last_name": "User",
        "email": "operator@test.com",
        "password": "secret",
        "role": Role.OPERATOR.value,
        "category_id": 1,
    }

    with pytest.raises(ValidationError):
        service.create_user(payload)

# create_user should create operator successfully
def test_create_user_operator_success():
    service = build_service()

    service.user_repository.get_by_username.return_value = None
    service.user_repository.get_by_email.return_value = None

    category = Mock()
    category.id = 10
    category.is_active = True

    service.category_repository.get_by_id.return_value = category

    payload = {
        "username": "operator",
        "first_name": "Test",
        "last_name": "User",
        "email": "operator@test.com",
        "password": "secret",
        "role": Role.OPERATOR.value,
        "category_id": 10,
    }

    result = service.create_user(payload)

    assert result.role == Role.OPERATOR
    assert result.category_id == 10

    service.user_repository.add.assert_called_once()
    service.session.commit.assert_called_once()

# update_user should reject duplicate username
def test_update_user_duplicate_username():
    service = build_service()

    user = make_user()

    service.user_repository.get_by_id.return_value = user
    service.user_repository.get_by_username.return_value = object()

    with pytest.raises(ValidationError):
        service.update_user(
            user.id,
            {"username": "taken"},
        )


# update_user should reject duplicate email
def test_update_user_duplicate_email():
    service = build_service()

    user = make_user()

    service.user_repository.get_by_id.return_value = user
    service.user_repository.get_by_email.return_value = object()

    with pytest.raises(ValidationError):
        service.update_user(
            user.id,
            {"email": "taken@test.com"},
        )


# update_user should update basic fields
def test_update_user_success():
    service = build_service()

    user = make_user()

    service.user_repository.get_by_id.return_value = user
    service.user_repository.get_by_username.return_value = None
    service.user_repository.get_by_email.return_value = None

    result = service.update_user(
        user.id,
        {
            "username": "newuser",
            "first_name": "New",
            "last_name": "Name",
            "email": "new@test.com",
        },
    )

    assert result.username == "newuser"
    assert result.first_name == "New"
    assert result.last_name == "Name"
    assert result.email == "new@test.com"

    service.session.commit.assert_called_once()


# update_user should update active flag and notifications
def test_update_user_flags():
    service = build_service()

    user = make_user()

    service.user_repository.get_by_id.return_value = user

    result = service.update_user(
        user.id,
        {
            "is_active": False,
            "email_notifications_enabled": False,
        },
    )

    assert result.is_active is False
    assert result.email_notifications_enabled is False


# update_user should change operator category
def test_update_user_operator_category():
    service = build_service()

    user = make_user(role=Role.CITIZEN)

    service.user_repository.get_by_id.return_value = user

    category = Mock()
    category.id = 5
    category.is_active = True

    service.category_repository.get_by_id.return_value = category

    result = service.update_user(
        user.id,
        {
            "role": Role.OPERATOR.value,
            "category_id": 5,
        },
    )

    assert result.role == Role.OPERATOR
    assert result.category_id == 5

# non-operator users should not require category
def test_resolve_operator_category_non_operator():
    service = build_service()

    result = service._resolve_operator_category(
        Role.CITIZEN,
        None,
    )

    assert result is None


# operator must provide category
def test_resolve_operator_category_missing():
    service = build_service()

    with pytest.raises(ValidationError):
        service._resolve_operator_category(
            Role.OPERATOR,
            None,
        )


# category id must be numeric
def test_resolve_operator_category_invalid_id():
    service = build_service()

    with pytest.raises(ValidationError):
        service._resolve_operator_category(
            Role.OPERATOR,
            "abc",
        )


# category must be active
def test_resolve_operator_category_inactive():
    service = build_service()

    category = Mock()
    category.is_active = False

    service.category_repository.get_by_id.return_value = category

    with pytest.raises(ValidationError):
        service._resolve_operator_category(
            Role.OPERATOR,
            1,
        )


# valid category should be returned
def test_resolve_operator_category_success():
    service = build_service()

    category = Mock()
    category.id = 5
    category.is_active = True

    service.category_repository.get_by_id.return_value = category

    result = service._resolve_operator_category(
        Role.OPERATOR,
        5,
    )

    assert result == category

# delete_account should anonymize and remove all user references
def test_delete_account_success():
    service = build_service()

    user = make_user(id=1)

    report = Mock()
    report.reporter_id = 1
    report.is_anonymous = False

    follower = Mock()

    sent_message = Mock()
    sent_message.sender_id = 1
    sent_message.recipient_id = 2

    received_message = Mock()
    received_message.sender_id = 3
    received_message.recipient_id = 1

    history = Mock()
    history.changed_by_id = 1

    notification = Mock()
    token = Mock()

    scalars_results = [
        [report],             # reports
        [follower],           # followers
        [sent_message, received_message],  # messages
        [history],            # histories
    ]

    service.session.scalars.side_effect = scalars_results

    service.notification_repository.list_for_user.return_value = [
        notification
    ]

    service.token_repository.list_for_user.return_value = [
        token
    ]

    service.delete_account(user)

    assert report.reporter_id is None
    assert report.is_anonymous is True

    assert sent_message.sender_id is None
    assert received_message.recipient_id is None

    assert history.changed_by_id is None

    service.user_repository.delete.assert_called_once_with(user)

    assert service.session.delete.call_count == 3
    service.session.commit.assert_called_once()

# update_profile should update names and notification preference
def test_update_profile_all_fields():
    service = build_service()

    user = make_user()

    result = service.update_profile(
        user,
        first_name="  John  ",
        last_name="  Doe  ",
        email_notifications_enabled=False,
    )

    assert result.first_name == "John"
    assert result.last_name == "Doe"
    assert result.email_notifications_enabled is False

    service.session.commit.assert_called_once()