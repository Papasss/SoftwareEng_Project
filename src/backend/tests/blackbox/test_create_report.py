# test_create_report.py

from __future__ import annotations

import pytest

from participium.services.report_service import ReportService


# BB table for create_report

"""
reporter        | category_id      | title                   | description            | latitude | longitude | photos              | is_anonymous | V/I | oracle
=========================================================================================================================================================================
valid user      | valid category   | "Broken streetlight"    | "Light not working"    | 45.0703  | 7.6869    | valid image list    | False        | V   | Report created successfully
valid user      | valid category   | "Road damage"           | "Large pothole"        | 45.0703  | 7.6869    | []                  | False        | V   | Report created without photos
valid user      | invalid category | "Garbage issue"         | "Overflowing bins"     | 45.0703  | 7.6869    | []                  | False        | I   | Invalid category ID
valid user      | valid category   | ""                      | "Description"          | 45.0703  | 7.6869    | []                  | False        | I   | Empty title error
valid user      | valid category   | "Water leakage"         | ""                     | 45.0703  | 7.6869    | []                  | False        | I   | Empty description error
valid user      | valid category   | "Traffic issue"         | "Heavy blockage"       | 999      | 7.6869    | []                  | False        | I   | Invalid latitude value
None            | valid category   | "Street issue"          | "Street blocked"       | 45.0703  | 7.6869    | []                  | False        | I   | User authentication required
valid user      | valid category   | "Illegal dumping"       | "Waste near road"      | 45.0703  | 7.6869    | invalid file type   | False        | I   | Unsupported file format
valid user      | valid category   | "Noise complaint"       | "Construction noise"   | 45.0703  | 7.6869    | valid image list    | True         | V   | Anonymous report created successfully
"""


@pytest.mark.skip(reason="Disabled.")
@pytest.mark.parametrize(
    "reporter,category_id,title,description,latitude,longitude,photos,is_anonymous,expected_exception,oracle",
    [
        ("valid_user", 1, "Broken streetlight", "Light not working", 45.0703, 7.6869, ["image.jpg"], False, None, "Report created successfully"),

        ("valid_user", 1, "Road damage", "Large pothole", 45.0703, 7.6869, [], False, None, "Report created without photos"),

        ("valid_user", -1, "Garbage issue", "Overflowing bins", 45.0703, 7.6869, [], False, Exception, "Invalid category ID"),

        ("valid_user", 1, "", "Description", 45.0703, 7.6869, [], False, Exception, "Empty title error"),

        ("valid_user", 1, "Water leakage", "", 45.0703, 7.6869, [], False, Exception, "Empty description error"),

        ("valid_user", 1, "Traffic issue", "Heavy blockage", 999, 7.6869, [], False, Exception, "Invalid latitude value"),

        (None, 1, "Street issue", "Street blocked", 45.0703, 7.6869, [], False, Exception, "User authentication required"),

        ("valid_user", 1, "Illegal dumping", "Waste near road", 45.0703, 7.6869, ["file.exe"], False, Exception, "Unsupported file format"),

        ("valid_user", 1, "Noise complaint", "Construction noise", 45.0703, 7.6869, ["image.jpg"], True, None, "Anonymous report created successfully"),
    ],
)
def test_suite_create_report(
    reporter,
    category_id,
    title,
    description,
    latitude,
    longitude,
    photos,
    is_anonymous,
    expected_exception,
    oracle,
):

    if expected_exception:
        with pytest.raises(expected_exception):
            ReportService.create_report(
                reporter,
                category_id,
                title,
                description,
                latitude,
                longitude,
                photos,
                is_anonymous,
            )

    else:
        result = ReportService.create_report(
            reporter,
            category_id,
            title,
            description,
            latitude,
            longitude,
            photos,
            is_anonymous,
        )

        assert result is not None