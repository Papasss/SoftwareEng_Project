# test_parse_date.py

from __future__ import annotations

import pytest

from participium.core.utils import parse_date


# BB table for parse_date

"""
value                   | V/I | oracle
========================================================
"2025-05-01"            | V   | Datetime object returned
None                    | V   | None returned
"invalid-date"          | I   | Invalid date format error
""                      | I   | Empty date value error
"2025/05/01"            | I   | Unsupported date format error
"""


@pytest.mark.skip(reason="Disabled.")
@pytest.mark.parametrize(
    "value,expected_exception,oracle",
    [
        ("2025-05-01", None, "Datetime object returned"),
        (None, None, "None returned"),
        ("invalid-date", Exception, "Invalid date format error"),
        ("", Exception, "Empty date value error"),
        ("2025/05/01", Exception, "Unsupported date format error"),
    ],
)
def test_suite_parse_date(value, expected_exception, oracle):

    if expected_exception:
        with pytest.raises(expected_exception):
            parse_date(value)

    else:
        result = parse_date(value)

        if oracle == "None returned":
            assert result is None

        else:
            assert result is not None