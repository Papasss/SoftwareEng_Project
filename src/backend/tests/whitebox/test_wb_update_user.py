from __future__ import annotations

from unittest.mock import Mock

import pytest

from participium.core.exceptions import ValidationError
from participium.models.category import Category
from participium.models.enums import Role
from participium.models.user import User
from participium.repositories.category_repository import CategoryRepository
from participium.repositories.notification_repository import NotificationRepository
from participium.repositories.token_repository import TokenRepository
from participium.repositories.user_repository import UserRepository
from participium.services.storage_service import StorageService
from participium.services.user_service import UserService


pytestmark = pytest.mark.whitebox


@pytest.fixture
def user_service_bundle() -> dict[str, object]:
    session = Mock()
    user_repository = Mock(spec=UserRepository)
    category_repository = Mock(spec=CategoryRepository)
    token_repository = Mock(spec=TokenRepository)
    notification_repository = Mock(spec=NotificationRepository)
    storage_service = Mock(spec=StorageService)
    service = UserService(
        session=session,
        user_repository=user_repository,
        category_repository=category_repository,
        token_repository=token_repository,
        notification_repository=notification_repository,
        storage_service=storage_service,
    )

    service.get_user = Mock()
    service._parse_role = Mock()  
    service._resolve_operator_category = Mock()  

    return {
        "service": service,
        "session": session,
        "user_repository": user_repository,
        "category_repository": category_repository,
        "token_repository": token_repository,
        "notification_repository": notification_repository,
        "storage_service": storage_service,
    }


@pytest.fixture
def reporter() -> User:
    return User(
        id=105,
        username="ajeje.brazorf",
        first_name="Ajeje",
        last_name="Brazorf",
        email="ajeje.brazorf@gmail.com",
        is_active=True,
        email_notifications_enabled=True,
        role=Role.CITIZEN,
    )


def test_update_user_raises_validation_error_when_username_already_in_use(
    user_service_bundle: dict[str, object],
    reporter: User,
) -> None:

    service = user_service_bundle["service"]
    user_repository = user_service_bundle["user_repository"]
    session = user_service_bundle["session"]
    service.get_user.return_value = reporter
    user_repository.get_by_username.return_value = User(id=106, username="fausto.gervasoni")

    with pytest.raises(ValidationError, match="Username already in use."):
        service.update_user(user_id=105, payload={"username": "fausto.gervasoni"})

    user_repository.get_by_username.assert_called_once_with("fausto.gervasoni")
    session.commit.assert_not_called()


def test_update_user_raises_validation_error_when_email_already_in_use(
    user_service_bundle: dict[str, object],
    reporter: User,
) -> None:

    service = user_service_bundle["service"]
    user_repository = user_service_bundle["user_repository"]
    session = user_service_bundle["session"]
    service.get_user.return_value = reporter
    user_repository.get_by_username.return_value = None
    user_repository.get_by_email.return_value = User(id=106, email="fausto.gervasoni@gmail.com")

    with pytest.raises(ValidationError, match="Email already in use."):
        service.update_user(user_id=105, payload={"email": "fausto.gervasoni@gmail.com"})

    user_repository.get_by_email.assert_called_once_with("fausto.gervasoni@gmail.com")
    session.commit.assert_not_called()


@pytest.mark.parametrize(
    "field,value,expected",
    [
        ("is_active", False, False),
        ("is_active", True, True),
        ("is_active", 0, False),
        ("is_active", 1, True),
        ("is_active", "false", True),
        ("is_active", "", False),
        ("email_notifications_enabled", False, False),
        ("email_notifications_enabled", True, True),
        ("email_notifications_enabled", 0, False),
        ("email_notifications_enabled", 1, True),
        ("email_notifications_enabled", "true", True),
        ("email_notifications_enabled", "", False),
    ],
)
def test_update_user_converts_boolean_fields_to_bool(
    user_service_bundle: dict[str, object],
    reporter: User,
    field: str,
    value: object,
    expected: bool,
) -> None:
    """Verifica che i campi booleani vengono convertiti a bool."""
    service = user_service_bundle["service"]
    user_repository = user_service_bundle["user_repository"]
    service.get_user.return_value = reporter
    user_repository.get_by_username.return_value = None
    user_repository.get_by_email.return_value = None

    service.update_user(user_id=105, payload={field: value})

    assert getattr(reporter, field) is expected


def test_update_user_parses_role(
    user_service_bundle: dict[str, object],
    reporter: User,
) -> None:
    
    service = user_service_bundle["service"]
    user_repository = user_service_bundle["user_repository"]
    service.get_user.return_value = reporter
    user_repository.get_by_username.return_value = None
    user_repository.get_by_email.return_value = None
    service._parse_role.return_value = Role.OPERATOR

    service.update_user(user_id=105, payload={"role": "operator"})

    service._parse_role.assert_called_once_with("operator")
    assert reporter.role == Role.OPERATOR


def test_update_user_resolves_category_when_role_changes(
    user_service_bundle: dict[str, object],
    reporter: User,
) -> None:

    service = user_service_bundle["service"]
    user_repository = user_service_bundle["user_repository"]
    service.get_user.return_value = reporter
    user_repository.get_by_username.return_value = None
    user_repository.get_by_email.return_value = None
    category_mock = Mock(spec=Category)
    category_mock.id = 2
    service._parse_role.return_value = Role.OPERATOR
    service._resolve_operator_category.return_value = category_mock

    service.update_user(user_id=105, payload={"role": "operator"})

    service._resolve_operator_category.assert_called_once_with(Role.OPERATOR, None)
    assert reporter.category_id == 2


def test_update_user_resolves_category_when_category_id_in_payload(
    user_service_bundle: dict[str, object],
    reporter: User,
) -> None:

    service = user_service_bundle["service"]
    user_repository = user_service_bundle["user_repository"]
    service.get_user.return_value = reporter
    user_repository.get_by_username.return_value = None
    user_repository.get_by_email.return_value = None
    category_mock = Mock(spec=Category)
    category_mock.id = 3
    service._resolve_operator_category.return_value = category_mock

    service.update_user(user_id=105, payload={"category_id": 3})

    service._resolve_operator_category.assert_called_once_with(Role.CITIZEN, 3)
    assert reporter.category_id == 3


def test_update_user_sets_category_id_to_none_if_category_not_resolved(
    user_service_bundle: dict[str, object],
    reporter: User,
) -> None:

    service = user_service_bundle["service"]
    user_repository = user_service_bundle["user_repository"]
    service.get_user.return_value = reporter
    user_repository.get_by_username.return_value = None
    user_repository.get_by_email.return_value = None
    service._resolve_operator_category.return_value = None

    service.update_user(user_id=105, payload={"category_id": 999})

    assert reporter.category_id is None


def test_update_user_complete_update_all_fields(
    user_service_bundle: dict[str, object],
    reporter: User,
) -> None:
    """Verifica un update completo di tutti i campi modificabili per l'utente 105."""
    service = user_service_bundle["service"]
    user_repository = user_service_bundle["user_repository"]
    session = user_service_bundle["session"]
    service.get_user.return_value = reporter
    user_repository.get_by_username.return_value = None
    user_repository.get_by_email.return_value = None

    category_mock = Mock(spec=Category)
    category_mock.id = 2
    service._parse_role.return_value = Role.OPERATOR
    service._resolve_operator_category.return_value = category_mock

    payload = {
        "username": "fausto.gervasoni",
        "first_name": "Giacomino",
        "last_name": "Poretti",
        "email": "fausto.gervasoni@gmail.com",
        "role": "operator",
        "category_id": 2,
        "is_active": True,
        "email_notifications_enabled": False,
    }

    result = service.update_user(user_id=105, payload=payload)

    assert result is reporter
    assert reporter.username == "fausto.gervasoni"
    assert reporter.first_name == "Giacomino"
    assert reporter.last_name == "Poretti"
    assert reporter.email == "fausto.gervasoni@gmail.com"
    assert reporter.role == Role.OPERATOR
    assert reporter.category_id == 2
    assert reporter.is_active is True
    assert reporter.email_notifications_enabled is False

    service.get_user.assert_called_once_with(105)
    user_repository.get_by_username.assert_called_once_with("fausto.gervasoni")
    user_repository.get_by_email.assert_called_once_with("fausto.gervasoni@gmail.com")
    service._parse_role.assert_called_once_with("operator")
    service._resolve_operator_category.assert_called_once_with(Role.OPERATOR, 2)
    session.commit.assert_called_once()

