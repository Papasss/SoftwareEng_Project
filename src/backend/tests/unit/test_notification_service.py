from unittest.mock import Mock

from participium.services.notification_service import NotificationService
from participium.models.enums import NotificationType, Role
from participium.models.notification import Notification
from participium.models.report import Report
from participium.models.user import User


def make_user(id=1, email_notifications_enabled=True):
    user = User(
        username="user",
        first_name="Test",
        last_name="User",
        email="user@test.com",
        password_hash="hash",
        role=Role.CITIZEN,
        email_notifications_enabled=email_notifications_enabled,
    )
    user.id = id
    return user


def make_report(id=1):
    report = Report(
        title="Report",
        description="Description",
        latitude=45.0,
        longitude=7.0,
        category_id=1,
    )
    report.id = id
    return report


def build_service():
    return NotificationService(
        session=Mock(),
        notification_repository=Mock(),
        email_gateway=Mock(),
    )


# notify_new_message should create a message notification
def test_notify_new_message():
    service = build_service()

    service.create_notification = Mock()

    recipient = make_user()
    report = make_report()

    service.notify_new_message(
        recipient,
        report,
        "Operator",
        "Hello citizen",
    )

    service.create_notification.assert_called_once()


# list_notifications should return repository result
def test_list_notifications():
    service = build_service()

    notifications = [Mock(), Mock()]

    service.notification_repository.list_for_user.return_value = notifications

    result = service.list_notifications(1)

    assert result == notifications


# unread notifications should be marked as read
def test_mark_report_message_notifications_as_read():
    service = build_service()

    notification1 = Notification(
        user_id=1,
        report_id=10,
        type=NotificationType.MESSAGE,
        title="A",
        body="B",
        is_read=False,
    )

    notification2 = Notification(
        user_id=1,
        report_id=10,
        type=NotificationType.MESSAGE,
        title="C",
        body="D",
        is_read=False,
    )

    service.notification_repository.list_unread_message_notifications.return_value = [
        notification1,
        notification2,
    ]

    result = service.mark_report_message_notifications_as_read(
        1,
        10,
    )

    assert result == 2
    assert notification1.is_read is True
    assert notification2.is_read is True

    service.session.commit.assert_called_once()


# no unread notifications should not commit
def test_mark_report_message_notifications_as_read_empty():
    service = build_service()

    service.notification_repository.list_unread_message_notifications.return_value = []

    result = service.mark_report_message_notifications_as_read(
        1,
        10,
    )

    assert result == 0

    service.session.commit.assert_not_called()


# notifications without report_id should be ignored
def test_count_unread_notifications_ignores_none_report():
    service = build_service()

    notification = Notification(
        user_id=1,
        report_id=None,
        type=NotificationType.MESSAGE,
        title="A",
        body="B",
        is_read=False,
    )

    service.notification_repository.list_unread_message_notifications.return_value = [
        notification
    ]

    result = service.count_unread_message_notifications_by_report(1)

    assert result == {}

# User should access own notification
def test_get_user_notification_success():
    service = build_service()

    notification = Mock()
    notification.user_id = 5

    service.notification_repository.get_by_id.return_value = notification

    result = service.get_user_notification(5, 10)

    assert result == notification

# Email sending should be skipped when disabled
def test_create_notification_email_disabled():
    service = build_service()

    user = make_user(
        email_notifications_enabled=False,
    )

    notification = service.create_notification(
        user,
        NotificationType.SYSTEM,
        "Title",
        "Body",
    )

    assert notification is not None

    service.email_gateway.send.assert_not_called()