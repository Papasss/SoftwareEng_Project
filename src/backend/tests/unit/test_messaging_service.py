from unittest.mock import Mock

import pytest

from participium.services.messaging_service import MessagingService
from participium.models.user import User
from participium.models.message import Message
from participium.core.exceptions import AuthorizationError
from participium.models.report import Report, ReportStatusHistory
from participium.models.enums import Role, ReportStatus

def make_user(id=1, role=Role.CITIZEN, category_id=None):
    user = User(
        username="user",
        first_name="Test",
        last_name="User",
        email="user@test.com",
        password_hash="hash",
        role=role,
    )
    user.id = id
    user.category_id = category_id
    return user


def make_report(id=1, reporter_id=1, category_id=1):
    report = Report(
        title="Report",
        description="Description",
        latitude=45,
        longitude=7,
        category_id=category_id,
    )
    report.id = id
    report.reporter_id = reporter_id
    report.status_history = []
    return report


def build_service():
    return MessagingService(
        session=Mock(),
        report_repository=Mock(),
        message_repository=Mock(),
        notification_service=Mock(),
    )


# list_messages should return repository messages
def test_list_messages():
    service = build_service()

    report = make_report(reporter_id=1)
    user = make_user(id=1)

    messages = [Mock(), Mock()]

    service.message_repository.list_for_report.return_value = messages

    result = service.list_messages(
        report,
        user,
    )

    assert result == messages


# unauthorized users should not access thread
def test_list_messages_access_denied():
    service = build_service()

    report = make_report(reporter_id=1)

    stranger = make_user(id=99)

    with pytest.raises(AuthorizationError):
        service.list_messages(
            report,
            stranger,
        )


# operator message recipient should be report reporter
def test_resolve_recipient_operator_returns_reporter():
    service = build_service()

    reporter = make_user(id=1)

    report = make_report()
    report.reporter = reporter

    operator = make_user(
        id=2,
        role=Role.OPERATOR,
    )

    recipient = service._resolve_recipient(
        report,
        operator,
    )

    assert recipient == reporter


# recipient can be resolved from previous messages
def test_resolve_recipient_from_message_history():
    service = build_service()

    operator = make_user(
        id=2,
        role=Role.OPERATOR,
    )

    message = Message(
        report_id=1,
        sender_id=operator.id,
        recipient_id=1,
        body="hello",
    )
    message.sender = operator

    service.message_repository.list_for_report.return_value = [
        message
    ]

    report = make_report()

    citizen = make_user(id=1)

    recipient = service._resolve_recipient(
        report,
        citizen,
    )

    assert recipient == operator

# non-operator message senders should be ignored
def test_resolve_recipient_ignores_non_operator_messages():
    service = build_service()

    citizen_sender = make_user(
        id=2,
        role=Role.CITIZEN,
    )

    message = Message(
        report_id=1,
        sender_id=citizen_sender.id,
        recipient_id=1,
        body="hello",
    )
    message.sender = citizen_sender

    service.message_repository.list_for_report.return_value = [
        message
    ]

    report = make_report()

    citizen = make_user(id=1)

    recipient = service._resolve_recipient(
        report,
        citizen,
    )

    assert recipient is None


# non-operator status history entries should be ignored
def test_resolve_recipient_ignores_non_operator_status_history():
    service = build_service()

    citizen_operator = make_user(
        id=3,
        role=Role.CITIZEN,
    )

    status_event = ReportStatusHistory(
        report_id=1,
        previous_status=None,
        new_status=ReportStatus.ASSIGNED,
        note="test",
        changed_by_id=citizen_operator.id,
    )

    status_event.changed_by = citizen_operator

    report = make_report()
    report.status_history = [status_event]

    service.message_repository.list_for_report.return_value = []

    citizen = make_user(id=1)

    recipient = service._resolve_recipient(
        report,
        citizen,
    )

    assert recipient is None