from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from participium.services.notification_service import NotificationService


pytestmark = pytest.mark.whitebox


# Structural tests for NotificationService.count_unread_message_notifications_by_report
# belong here. The current runnable smoke check is kept in test_wb_task06_smoke.py.


def test_returns_empty_dictionary_when_notifications_list_is_empty():
    repository = Mock()
    repository.list_unread_message_notifications.return_value = []

    service = NotificationService(
        notification_repository=repository,
    )

    result = service.count_unread_message_notifications_by_report(user_id=1)

    assert result == {}


def test_skips_notifications_with_none_report_id():
    notification = SimpleNamespace(
        report_id=None,
    )

    repository = Mock()
    repository.list_unread_message_notifications.return_value = [notification]

    service = NotificationService(
        notification_repository=repository,
    )

    result = service.count_unread_message_notifications_by_report(user_id=1)

    assert result == {}


def test_initializes_count_for_first_report_occurrence():
    notification = SimpleNamespace(
        report_id=10,
    )

    repository = Mock()
    repository.list_unread_message_notifications.return_value = [notification]

    service = NotificationService(
        notification_repository=repository,
    )

    result = service.count_unread_message_notifications_by_report(user_id=1)

    assert result == {10: 1}


def test_increments_count_for_duplicate_report_id():
    notifications = [
        SimpleNamespace(report_id=10),
        SimpleNamespace(report_id=10),
    ]

    repository = Mock()
    repository.list_unread_message_notifications.return_value = notifications

    service = NotificationService(
        notification_repository=repository,
    )

    result = service.count_unread_message_notifications_by_report(user_id=1)

    assert result == {10: 2}
