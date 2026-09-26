# test_send_message.py

from __future__ import annotations

import pytest

from participium.services.messaging_service import MessagingService


# BB table for send_message

"""
report              | sender              | body                         | V/I | oracle
===========================================================================================================
valid report        | valid user          | "Issue still unresolved"    | V   | Message sent successfully
valid report        | valid user          | ""                          | I   | Empty message error
closed report       | valid user          | "Need update"               | I   | Messaging not allowed for closed report
invalid report      | valid user          | "Any update?"               | I   | Report not found
valid report        | unauthorized user   | "Checking status"           | I   | User authorization required
valid report        | valid user          | very long message           | V   | Message sent successfully
valid report        | None                | "Test message"              | I   | User authentication required
"""


@pytest.mark.skip(reason="Disabled.")
@pytest.mark.parametrize(
    "report,sender,body,expected_exception,oracle",
    [
        ("valid_report", "valid_user", "Issue still unresolved", None, "Message sent successfully"),

        ("valid_report", "valid_user", "", Exception, "Empty message error"),

        ("closed_report", "valid_user", "Need update", Exception, "Messaging not allowed for closed report"),

        ("invalid_report", "valid_user", "Any update?", Exception, "Report not found"),

        ("valid_report", "unauthorized_user", "Checking status", Exception, "User authorization required"),

        ("valid_report", "valid_user", "very long message", None, "Message sent successfully"),

        ("valid_report", None, "Test message", Exception, "User authentication required"),
    ],
)
def test_suite_send_message(
    report,
    sender,
    body,
    expected_exception,
    oracle,
):

    if expected_exception:
        with pytest.raises(expected_exception):
            MessagingService.send_message(
                report,
                sender,
                body,
            )

    else:
        result = MessagingService.send_message(
            report,
            sender,
            body,
        )

        assert result is not None