from __future__ import annotations

from datetime import datetime, timedelta
from io import BytesIO
from unittest.mock import Mock

import pytest
from werkzeug.datastructures import FileStorage

from participium.core.exceptions import AuthorizationError, AuthenticationError, NotFoundError, ValidationError
from participium.core.security import hash_password
from participium.models.enums import NotificationType, ReportStatus, Role
from participium.models.message import Message
from participium.models.notification import Notification
from participium.models.report import Report, ReportStatusHistory
from participium.models.user import User
from participium.models.token import EmailVerificationToken
from participium.services.auth_service import AuthService
from participium.services.messaging_service import MessagingService
from participium.services.notification_service import NotificationService


def make_user(**overrides) -> User:
    defaults = {
        "username": "tester",
        "first_name": "Test",
        "last_name": "User",
        "email": "tester@example.com",
        "password_hash": hash_password("secret"),
        "role": Role.CITIZEN,
        "is_active": True,
        "is_email_verified": True,
        "email_notifications_enabled": True,
    }
    defaults.update(overrides)
    return User(**defaults)


def make_report(**overrides) -> Report:
    defaults = {
        "title": "Sample report",
        "description": "A problem has been detected.",
        "latitude": 45.0,
        "longitude": 7.0,
        "status": ReportStatus.PENDING_APPROVAL,
        "is_anonymous": False,
        "reporter_id": 1,
        "category_id": 1,
    }
    defaults.update(overrides)
    return Report(**defaults)


class DummyStorageService:
    def save(self, file: FileStorage) -> str:
        return f"saved-{file.filename}"


class DummyNotificationService:
    def __init__(self):
        self.calls = []

    def notify_new_message(self, recipient, report, sender_name, body):
        self.calls.append((recipient, report, sender_name, body))


def test_auth_service_register_user_successful_email_and_verification_url():
    session = Mock()
    session.flush = Mock()
    session.commit = Mock()

    user_repository = Mock()
    user_repository.get_by_username.return_value = None
    user_repository.get_by_email.return_value = None
    user_repository.add = Mock()

    token_repository = Mock()
    token_repository.add = Mock()
    email_gateway = Mock()

    service = AuthService(session, user_repository, token_repository, email_gateway)
    payload = {
        "username": "newuser",
        "first_name": "New",
        "last_name": "User",
        "email": "newuser@example.com",
        "password": "StrongPass123",
    }

    user, verification_url = service.register_user(payload, "http://example.com/verify")

    assert user.username == "newuser"
    assert user.email == "newuser@example.com"
    assert verification_url is not None
    assert verification_url.startswith("http://example.com/verify/")
    email_gateway.send.assert_called_once()
    token_repository.add.assert_called_once()


def test_auth_service_register_user_missing_required_fields():
    session = Mock()
    service = AuthService(session, Mock(), Mock(), Mock())

    with pytest.raises(ValidationError, match="Missing required fields"):
        service.register_user({"username": ""})


def test_auth_service_verify_email_invalid_and_expired_token():
    session = Mock()
    token_repository = Mock()
    token_repository.get_by_token.return_value = None
    service = AuthService(session, Mock(), token_repository, Mock())

    with pytest.raises(ValidationError, match="Verification token is invalid"):
        service.verify_email("missing-token")

    token = EmailVerificationToken(
        user_id=1,
        token="token-123",
        expires_at=datetime.utcnow() - timedelta(hours=1),
        is_used=False,
    )
    token.user = make_user()
    token_repository.get_by_token.return_value = token

    with pytest.raises(ValidationError, match="Verification token has expired"):
        service.verify_email("token-123")


def test_auth_service_authenticate_raises_for_invalid_credentials_and_unverified_email():
    session = Mock()
    user = make_user(password_hash=hash_password("correct"), is_email_verified=False)
    repository = Mock()
    repository.get_by_username_or_email.return_value = user

    service = AuthService(session, repository, Mock(), Mock())

    with pytest.raises(AuthenticationError, match="Invalid credentials"):
        service.authenticate("tester", "wrong")

    with pytest.raises(AuthenticationError, match="Email verification is required"):
        service.authenticate("tester", "correct")


def test_notification_service_create_and_handle_email_failure():
    session = Mock()
    repository = Mock(add=Mock())
    email_gateway = Mock()
    email_gateway.send.side_effect = Exception("send failed")

    user = make_user(email_notifications_enabled=True)
    service = NotificationService(session=session, notification_repository=repository, email_gateway=email_gateway)

    notification = service.create_notification(user, NotificationType.SYSTEM, "Hello", "World")

    assert isinstance(notification, Notification)
    assert notification.user_id == user.id
    email_gateway.send.assert_called_once()


def test_notification_service_skip_user_and_count_unread_notifications():
    session = Mock()
    repository = Mock()
    repository.list_unread_message_notifications.return_value = [
        Notification(user_id=1, report_id=2, type=NotificationType.MESSAGE, title="A", body="B", is_read=False),
        Notification(user_id=1, report_id=2, type=NotificationType.MESSAGE, title="A", body="B", is_read=False),
    ]
    service = NotificationService(session=session, notification_repository=repository, email_gateway=Mock())

    assert service.create_notification(None, NotificationType.SYSTEM, "x", "y") is None
    counts = service.count_unread_message_notifications_by_report(1)
    assert counts == {2: 2}


def test_notification_service_mark_as_read_and_access_checks():
    session = Mock()
    repository = Mock()
    notification = Notification(user_id=5, report_id=None, type=NotificationType.SYSTEM, title="x", body="y", is_read=False)
    repository.get_by_id.return_value = notification

    service = NotificationService(session=session, notification_repository=repository, email_gateway=Mock())
    result = service.mark_as_read(notification)

    assert result.is_read is True
    session.commit.assert_called_once()

    with pytest.raises(NotFoundError, match="Notification not found"):
        repository.get_by_id.return_value = None
        service.get_user_notification(5, 10)

    with pytest.raises(AuthorizationError):
        repository.get_by_id.return_value = Notification(user_id=7, report_id=None, type=NotificationType.SYSTEM, title="x", body="y", is_read=False)
        service.get_user_notification(5, 10)


def test_notification_service_notify_status_change_deduplicates():
    reporter = make_user(id=1)
    duplicate = make_user(id=1)
    report = make_report(id=1)
    service = NotificationService(session=Mock(), notification_repository=Mock(), email_gateway=Mock())
    service.create_notification = Mock()

    service.notify_status_change([reporter, duplicate, None], report, "body")

    service.create_notification.assert_called_once()


def test_messaging_service_access_and_send_message_branches():
    report = make_report(id=42, reporter_id=10, category_id=1)
    reporter = make_user(id=10, role=Role.CITIZEN)
    operator = make_user(id=2, role=Role.OPERATOR, category_id=1)
    admin = make_user(id=3, role=Role.ADMIN)
    report.reporter = reporter

    message_repository = Mock()
    message_repository.list_for_report.return_value = []

    service = MessagingService(
        session=Mock(commit=Mock()),
        report_repository=Mock(),
        message_repository=message_repository,
        notification_service=Mock(notify_new_message=Mock()),
    )

    assert service.can_access_thread(report, admin) is True
    assert service.can_access_thread(report, operator) is True
    assert service.can_access_thread(report, reporter) is True
    assert service.can_access_thread(report, None) is False

    with pytest.raises(ValidationError, match="Message body cannot be empty"):
        service.send_message(report, reporter, "   ")

    service.message_repository.list_for_report.return_value = []
    with pytest.raises(ValidationError, match="No recipient available"):
        service.send_message(report, reporter, "Hello")

    # When an operator sends a message, the recipient is the reporter.
    service.message_repository.list_for_report.return_value = []
    message_sender = operator
    message = Message(report_id=report.id, sender_id=operator.id, recipient_id=reporter.id, body="Hello")
    service.message_repository.add = Mock(return_value=message)
    result = service.send_message(report, message_sender, "Hello world")

    assert result.body == "Hello world"
    service.message_repository.add.assert_called_once()
    service.notification_service.notify_new_message.assert_called_once()


def test_messaging_service_resolve_recipient_from_history():
    report = make_report(id=42)
    reporter = make_user(id=10, role=Role.CITIZEN)
    operator = make_user(id=2, role=Role.OPERATOR, category_id=1)
    report.reporter = reporter
    report.category_id = 1
    report.status_history = [ReportStatusHistory(report_id=42, previous_status=None, new_status=ReportStatus.ASSIGNED, note="", changed_by_id=2)]
    report.status_history[0].changed_by = operator

    message_repository = Mock()
    message_repository.list_for_report.return_value = []

    service = MessagingService(
        session=Mock(),
        report_repository=Mock(),
        message_repository=message_repository,
        notification_service=Mock(notify_new_message=Mock()),
    )

    recipient = service._resolve_recipient(report, reporter)
    assert recipient == operator


def test_sender_name_falls_back_to_username():
    sender = make_user(first_name="", last_name="", username="fallback")
    assert MessagingService._sender_name(sender) == "fallback"
