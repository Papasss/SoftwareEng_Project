from __future__ import annotations

import pytest

from participium.services.report_service import ReportService


# BB table for list_public_reports

"""
category_id       | status            | date_from         | date_to           | sort              | V/I | oracle
================================================================================================================================================================
None              | None              | None              | None              | "desc"            | V   | Public reports returned successfully
valid category    | None              | None              | None              | "desc"            | V   | Reports filtered by category
None              | "Resolved"        | None              | None              | "desc"            | V   | Resolved reports returned
None              | None              | valid start date  | valid end date    | "desc"            | V   | Reports filtered by date range
None              | None              | None              | None              | "asc"             | V   | Reports sorted in ascending order
invalid category  | None              | None              | None              | "desc"            | I   | Invalid category ID
None              | invalid status    | None              | None              | "desc"            | I   | Invalid report status
None              | None              | future date       | past date         | "desc"            | I   | Invalid date range
None              | None              | None              | None              | invalid sort      | I   | Invalid sorting option
"""


@pytest.mark.parametrize(
    "category_id,status,date_from,date_to,sort,expected_exception,oracle",
    [
        (None, None, None, None, "desc", None, "Public reports returned successfully"),

        (1, None, None, None, "desc", None, "Reports filtered by category"),

        (None, "Resolved", None, None, "desc", None, "Resolved reports returned"),

        (None, None, "2025-01-01", "2025-12-31", "desc", None, "Reports filtered by date range"),

        (None, None, None, None, "asc", None, "Reports sorted in ascending order"),

        (-1, None, None, None, "desc", Exception, "Invalid category ID"),

        (None, "invalid_status", None, None, "desc", Exception, "Invalid report status"),

        (None, None, "2030-01-01", "2020-01-01", "desc", Exception, "Invalid date range"),

        (None, None, None, None, "random", Exception, "Invalid sorting option"),
    ],
)
def test_suite_list_public_reports(
    category_id,
    status,
    date_from,
    date_to,
    sort,
    expected_exception,
    oracle,
):

    if expected_exception:
        with pytest.raises(expected_exception):
            ReportService.list_public_reports(
                category_id,
                status,
                date_from,
                date_to,
                sort,
            )

    else:
        result = ReportService.list_public_reports(
            category_id,
            status,
            date_from,
            date_to,
            sort,
        )

        assert result is not None