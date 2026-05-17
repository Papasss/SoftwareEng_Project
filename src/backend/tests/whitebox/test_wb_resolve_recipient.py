from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from participium.models.enums import Role
from participium.services.messaging_service import MessagingService


pytestmark = pytest.mark.whitebox


# Structural tests for MessagingService._resolve_recipient belong here.
# The current runnable smoke check is kept in test_wb_task06_smoke.py.


def _user(user_id: int, role: Role):
    return SimpleNamespace(
        id=user_id,
        role=role,
    )


def test_admin_sender_returns_reporter():
    reporter = _user(1, Role.REPORTER)
    sender = _user(2, Role.ADMIN)

    report = SimpleNamespace(
        id=100,
        reporter=reporter,
        status_history=[],
    )

    service = MessagingService(
        message_repository=Mock(),
    )

    result = service._resolve_recipient(report, sender)

    assert result == reporter


def test_previous_operator_message_used():
    sender = _user(1, Role.REPORTER)
    operator = _user(2, Role.OPERATOR)

    old_message = SimpleNamespace(
        sender=operator,
    )

    repository = Mock()
    repository.list_for_report.return_value = [old_message]

    report = SimpleNamespace(
        id=100,
        reporter=None,
        status_history=[],
    )

    service = MessagingService(
        message_repository=repository,
    )

    result = service._resolve_recipient(report, sender)

    assert result == operator
    repository.list_for_report.assert_called_once_with(100)


def test_status_history_operator_used():
    sender = _user(1, Role.REPORTER)
    operator = _user(2, Role.OPERATOR)

    status_event = SimpleNamespace(
        changed_by=operator,
    )

    repository = Mock()
    repository.list_for_report.return_value = []

    report = SimpleNamespace(
        id=100,
        reporter=None,
        status_history=[status_event],
    )

    service = MessagingService(
        message_repository=repository,
    )

    result = service._resolve_recipient(report, sender)

    assert result == operator


def test_no_recipient_returns_none():
    sender = _user(1, Role.REPORTER)

    repository = Mock()
    repository.list_for_report.return_value = []

    status_event = SimpleNamespace(
        changed_by=None,
    )

    report = SimpleNamespace(
        id=100,
        reporter=None,
        status_history=[status_event],
    )

    service = MessagingService(
        message_repository=repository,
    )

    result = service._resolve_recipient(report, sender)

    assert result is None