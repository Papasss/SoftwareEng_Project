from __future__ import annotations

import pytest

from participium.core.exceptions import ValidationError, AuthorizationError, NotFoundError
from participium.models.user import User
from participium.services.report_service import ReportService
from participium.models.enums import ReportStatus
from participium.models.report import Report

ADMIN_USER = User(
    id=105,
    username="ajeje.brazorf",
    first_name="Aldo",
    last_name="Baglio",
    role="admin",
    is_active=True,
    category_id=1
)

OPERATOR_USER = User(
    id=106,
    username="fausto.gervasoni",
    first_name="Giacomino",
    last_name="Poretti",
    role="operator",
    is_active=True,
    category_id=2
)

CITIZEN_USER = User(
    id=107,
    username="ignazio.ilsurname",
    first_name="Giovanni",
    last_name="Storti",
    role="citizen",
    is_active=True,
    category_id=2
)

report = Report(
    id=201,
    title="Buco in strada",
    description="C'è un buco profondo in mezzo alla strada.",
    latitude=45.4642,
    longitude=9.1900,
    status=ReportStatus.PENDING_APPROVAL,
    reporter_id=CITIZEN_USER.id,
    category_id=2
)

# USER NOT ALLOWED
@pytest.mark.skip(reason="Disabled.")
def test_verify_user_not_allowed() -> None:
    report_service = ReportService()

    with pytest.raises(AuthorizationError):
        report_service.update_status(report_id=report.id, operator=CITIZEN_USER, next_status_value=ReportStatus.ASSIGNED)


# REPORT NOT IN THE SAME CATEGORY AS OPERATOR
@pytest.mark.skip(reason="Disabled.")
def test_verify_report_not_in_same_category() -> None:
    report_service = ReportService()

    with pytest.raises(AuthorizationError):
        report_service.update_status(report_id=report.id, operator=ADMIN_USER, next_status_value=ReportStatus.ASSIGNED)


# REPORT NOT EXISTS
@pytest.mark.skip(reason="Disabled.")
def test_verify_report_not_exists() -> None:
    report_service = ReportService()

    with pytest.raises(NotFoundError):
        report_service.update_status(report_id=5, operator=OPERATOR_USER, next_status_value=ReportStatus.ASSIGNED)


# NEXT STATUS IS NOT VALID
@pytest.mark.skip(reason="Disabled.")
def test_verify_next_status_not_valid() -> None:
    report_service = ReportService()

    with pytest.raises(ValidationError):
        report_service.update_status(report_id=report.id, operator=OPERATOR_USER, next_status_value="INVALID_STATUS")


# REJECTION WITHOUT NOTE
@pytest.mark.skip(reason="Disabled.")
def test_verify_rejection_without_note() -> None:
    report_service = ReportService()

    with pytest.raises(ValidationError):
        report_service.update_status(report_id=report.id, operator=OPERATOR_USER, next_status_value=ReportStatus.REJECTED)


# TRANSITION NOT ALLOWED (E.G., FROM PENDING_APPROVAL TO RESOLVED)
@pytest.mark.skip(reason="Disabled.")
def test_verify_transition_not_allowed() -> None:
    report_service = ReportService()

    with pytest.raises(ValidationError):
        report_service.update_status(report_id=report.id, operator=OPERATOR_USER, next_status_value=ReportStatus.RESOLVED)