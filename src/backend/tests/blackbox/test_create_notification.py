# test_create_notification.py

from __future__ import annotations

import pytest

from participium.services.notification_service import NotificationService


# BB table for create_notification

"""
user            | notification_type   | title                   | body                           | report          | V/I | oracle
=================================================================================================================================================================
valid user      | valid type          | "Report updated"        | "Your report status changed"   | valid report    | V   | Notification created successfully
None            | system type         | "Maintenance notice"    | "System update tonight"        | None            | V   | System notification created successfully
valid user      | invalid type        | "Alert"                 | "Test notification"            | None            | I   | Invalid notification type
valid user      | valid type          | ""                      | "Notification body"            | None            | I   | Empty notification title
valid user      | valid type          | "Reminder"              | ""                             | None            | I   | Empty notification body
valid user      | valid type          | "Status update"         | very long message              | valid report    | V   | Notification created successfully
invalid user    | valid type          | "Warning"               | "Unauthorized access"          | None            | I   | Invalid user account
"""


@pytest.mark.skip(reason="Disabled.")
@pytest.mark.parametrize(
    "user,notification_type,title,body,report,expected_exception,oracle",
    [
        ("valid_user", "valid_type", "Report updated", "Your report status changed", "valid_report", None, "Notification created successfully"),

        (None, "system_type", "Maintenance notice", "System update tonight", None, None, "System notification created successfully"),

        ("valid_user", "invalid_type", "Alert", "Test notification", None, Exception, "Invalid notification type"),

        ("valid_user", "valid_type", "", "Notification body", None, Exception, "Empty notification title"),

        ("valid_user", "valid_type", "Reminder", "", None, Exception, "Empty notification body"),

        ("valid_user", "valid_type", "Status update", "very long message", "valid_report", None, "Notification created successfully"),

        ("invalid_user", "valid_type", "Warning", "Unauthorized access", None, Exception, "Invalid user account"),
    ],
)
def test_suite_create_notification(
    user,
    notification_type,
    title,
    body,
    report,
    expected_exception,
    oracle,
):

    if expected_exception:
        with pytest.raises(expected_exception):
            NotificationService.create_notification(
                user,
                notification_type,
                title,
                body,
                report,
            )

    else:
        result = NotificationService.create_notification(
            user,
            notification_type,
            title,
            body,
            report,
        )

        assert result is not None