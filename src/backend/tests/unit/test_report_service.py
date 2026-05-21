from unittest.mock import Mock
from io import BytesIO

import pytest
from werkzeug.datastructures import FileStorage

from participium.services.report_service import ReportService
from participium.models.enums import ReportStatus, Role
from participium.models.report import Report
from participium.models.user import User
from participium.core.exceptions import (
    ValidationError,
    NotFoundError,
    AuthorizationError,
)

# Create a test user
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


# Create a test report
def make_report(
    id=1,
    status=ReportStatus.PENDING_APPROVAL,
    category_id=1,
    reporter_id=1,
):
    report = Report(
        title="Broken road",
        description="Road damage",
        latitude=45.0,
        longitude=7.0,
        category_id=category_id,
    )

    report.id = id
    report.status = status
    report.reporter_id = reporter_id
    report.followers = []

    return report


# Create a fake uploaded image
def make_photo(filename="photo.jpg"):
    return FileStorage(
        stream=BytesIO(b"fake-image"),
        filename=filename,
        content_type="image/jpeg",
    )


# Build ReportService with mocked dependencies
def build_service():
    return ReportService(
        session=Mock(),
        report_repository=Mock(),
        category_repository=Mock(),
        storage_service=Mock(),
        notification_service=Mock(),
    )


# Report should be returned when it exists
def test_get_report_success():
    service = build_service()

    report = make_report()

    service.report_repository.get_by_id.return_value = report

    result = service.get_report(1)

    assert result == report


# NotFoundError should be raised for unknown report
def test_get_report_not_found():
    service = build_service()

    service.report_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        service.get_report(999)


# Invalid category should be rejected
def test_create_report_invalid_category():
    service = build_service()

    service.category_repository.get_by_id.return_value = None

    with pytest.raises(ValidationError):
        service.create_report(
            reporter=make_user(),
            category_id=1,
            title="title",
            description="description",
            latitude=45,
            longitude=7,
            photos=[make_photo()],
        )


# Missing title should raise ValidationError
def test_create_report_missing_title():
    service = build_service()

    category = Mock()
    category.id = 1
    category.is_active = True

    service.category_repository.get_by_id.return_value = category

    with pytest.raises(ValidationError):
        service.create_report(
            reporter=make_user(),
            category_id=1,
            title=None,
            description="description",
            latitude=45,
            longitude=7,
            photos=[make_photo()],
        )


# Invalid coordinates should raise ValidationError
def test_create_report_invalid_coordinates():
    service = build_service()

    category = Mock()
    category.id = 1
    category.is_active = True

    service.category_repository.get_by_id.return_value = category

    with pytest.raises(ValidationError):
        service.create_report(
            reporter=make_user(),
            category_id=1,
            title="title",
            description="description",
            latitude="abc",
            longitude="xyz",
            photos=[make_photo()],
        )


# Report must contain at least one photo
def test_create_report_requires_photo():
    service = build_service()

    category = Mock()
    category.id = 1
    category.is_active = True

    service.category_repository.get_by_id.return_value = category

    with pytest.raises(ValidationError):
        service.create_report(
            reporter=make_user(),
            category_id=1,
            title="title",
            description="description",
            latitude=45,
            longitude=7,
            photos=[],
        )


# Maximum number of photos is three
def test_create_report_too_many_photos():
    service = build_service()

    category = Mock()
    category.id = 1
    category.is_active = True

    service.category_repository.get_by_id.return_value = category

    photos = [
        make_photo(),
        make_photo(),
        make_photo(),
        make_photo(),
    ]

    with pytest.raises(ValidationError):
        service.create_report(
            reporter=make_user(),
            category_id=1,
            title="title",
            description="description",
            latitude=45,
            longitude=7,
            photos=photos,
        )


# Report should be created successfully with valid data
def test_create_report_success():
    service = build_service()

    category = Mock()
    category.id = 1
    category.is_active = True

    service.category_repository.get_by_id.return_value = category

    report = make_report()

    service.report_repository.get_by_id.return_value = report
    service.storage_service.save.return_value = "saved-photo.jpg"

    result = service.create_report(
        reporter=make_user(),
        category_id=1,
        title="Road issue",
        description="Broken road",
        latitude=45,
        longitude=7,
        photos=[make_photo()],
    )

    assert result == report

    service.report_repository.add.assert_called_once()
    service.report_repository.add_photo.assert_called_once()
    service.report_repository.add_status_entry.assert_called_once()

# Public reports should be accessible without authentication
def test_get_accessible_report_public():
    service = build_service()

    report = make_report(status=ReportStatus.RESOLVED)

    service.report_repository.get_by_id.return_value = report

    result = service.get_accessible_report(1)

    assert result == report


# Reporter should access their own report
def test_get_accessible_report_reporter():
    service = build_service()

    report = make_report(reporter_id=1)

    service.report_repository.get_by_id.return_value = report

    result = service.get_accessible_report(1, make_user(id=1))

    assert result == report


# Admin should access every report
def test_get_accessible_report_admin():
    service = build_service()

    report = make_report()

    service.report_repository.get_by_id.return_value = report

    admin = make_user(id=99, role=Role.ADMIN)

    result = service.get_accessible_report(1, admin)

    assert result == report


# Unauthorized user should not access another private report
def test_get_accessible_report_denied():
    service = build_service()

    report = make_report(reporter_id=1)

    service.report_repository.get_by_id.return_value = report

    user = make_user(id=99)

    with pytest.raises(AuthorizationError):
        service.get_accessible_report(1, user)


# Following a non-public report should fail
def test_follow_report_not_public():
    service = build_service()

    report = make_report(status=ReportStatus.PENDING_APPROVAL)

    service.report_repository.get_by_id.return_value = report

    with pytest.raises(ValidationError):
        service.follow_report(1, make_user())


# Existing follower should not be added again
def test_follow_report_already_following():
    service = build_service()

    report = make_report(status=ReportStatus.RESOLVED)

    service.report_repository.get_by_id.return_value = report

    service.report_repository.get_follower.return_value = object()

    result = service.follow_report(1, make_user())

    assert result == report

    service.report_repository.add_follower.assert_not_called()


# Existing follower should be removable
def test_unfollow_report_existing_follower():
    service = build_service()

    report = make_report(status=ReportStatus.RESOLVED)

    service.report_repository.get_by_id.return_value = report

    follower = object()

    service.report_repository.get_follower.return_value = follower

    result = service.unfollow_report(1, make_user())

    assert result == report

    service.report_repository.remove_follower.assert_called_once_with(follower)


# Resolved reports should be public
def test_is_public():
    report = make_report(status=ReportStatus.RESOLVED)

    assert ReportService.is_public(report) is True

# Following a public report should create a follower
def test_follow_report_success():
    service = build_service()

    report = make_report(status=ReportStatus.RESOLVED)

    service.report_repository.get_by_id.return_value = report
    service.report_repository.get_follower.return_value = None

    result = service.follow_report(1, make_user())

    assert result == report

    service.report_repository.add_follower.assert_called_once()
    service.session.commit.assert_called_once()


# Unfollow should do nothing if follower does not exist
def test_unfollow_report_without_existing_follower():
    service = build_service()

    report = make_report(status=ReportStatus.RESOLVED)

    service.report_repository.get_by_id.return_value = report
    service.report_repository.get_follower.return_value = None

    result = service.unfollow_report(1, make_user())

    assert result == report

    service.report_repository.remove_follower.assert_not_called()

# Reporter alone should be returned as recipient
def test_recipients_returns_reporter():
    report = Mock()

    reporter = make_user(id=1)

    report.reporter = reporter
    report.followers = []

    recipients = ReportService._recipients(report)

    assert recipients == [reporter]


# None reporter should be filtered out
def test_recipients_filters_none_reporter():
    report = Mock()

    report.reporter = None
    report.followers = []

    recipients = ReportService._recipients(report)

    assert recipients == []

# Admin should always pass category access check
def test_operator_category_access_admin():
    admin = make_user(role=Role.ADMIN)

    report = make_report(category_id=10)

    ReportService._ensure_operator_category_access(admin, report)


# Operator with matching category should pass
def test_operator_category_access_matching_category():
    operator = make_user(
        role=Role.OPERATOR,
        category_id=1,
    )

    report = make_report(category_id=1)

    ReportService._ensure_operator_category_access(operator, report)


# Operator with different category should fail
def test_operator_category_access_wrong_category():

    operator = make_user(
        role=Role.OPERATOR,
        category_id=99,
    )

    report = make_report(category_id=1)

    with pytest.raises(AuthorizationError):
        ReportService._ensure_operator_category_access(
            operator,
            report,
        )

# assign_report should reject non operator/admin users
def test_assign_report_requires_operator():
    service = build_service()

    citizen = make_user(role=Role.CITIZEN)

    with pytest.raises(AuthorizationError):
        service.assign_report(1, citizen)


# assign_report should reject reports not in pending state
def test_assign_report_requires_pending_report():
    service = build_service()

    operator = make_user(
        role=Role.OPERATOR,
        category_id=1,
    )

    report = make_report(
        status=ReportStatus.RESOLVED,
        category_id=1,
    )

    report.category = Mock()
    report.category.name = "Roads"

    service.report_repository.get_by_id.return_value = report

    with pytest.raises(ValidationError):
        service.assign_report(1, operator)


# update_status should reject invalid status values
def test_update_status_invalid_status():
    service = build_service()

    operator = make_user(
        role=Role.OPERATOR,
        category_id=1,
    )

    report = make_report(category_id=1)

    service.report_repository.get_by_id.return_value = report

    with pytest.raises(ValidationError):
        service.update_status(
            1,
            operator,
            "INVALID_STATUS",
        )


# update_status reject without note
def test_update_status_rejected_without_reason():
    service = build_service()

    operator = make_user(
        role=Role.OPERATOR,
        category_id=1,
    )

    report = make_report(category_id=1)

    service.report_repository.get_by_id.return_value = report

    with pytest.raises(ValidationError):
        service.update_status(
            1,
            operator,
            ReportStatus.REJECTED.value,
        )


# export_rows should serialize report fields
def test_export_rows_success():
    service = build_service()

    report = make_report(
        status=ReportStatus.RESOLVED,
    )

    report.category = Mock()
    report.category.name = "Roads"

    report.created_at = Mock()
    report.created_at.isoformat.return_value = "2025-01-01"

    service.report_repository.list_reports.return_value = [report]

    rows = service.export_rows()

    assert len(rows) == 1

    assert rows[0]["id"] == report.id
    assert rows[0]["title"] == report.title
    assert rows[0]["category"] == "Roads"
    assert rows[0]["status"] == report.status.value

# Operator can successfully assign a pending report
def test_assign_report_success():
    service = build_service()

    operator = make_user(
        id=10,
        role=Role.OPERATOR,
        category_id=1,
    )

    report = make_report(
        id=1,
        category_id=1,
        status=ReportStatus.PENDING_APPROVAL,
    )

    report.category = Mock()
    report.category.name = "Roads"

    service.report_repository.get_by_id.return_value = report

    result = service.assign_report(1, operator)

    assert result == report
    assert report.status == ReportStatus.ASSIGNED

    service.report_repository.add_status_entry.assert_called_once()
    service.notification_service.notify_status_change.assert_called_once()
    service.session.commit.assert_called_once()


# Only operators/admins can update status
def test_update_status_requires_operator():
    service = build_service()

    citizen = make_user(role=Role.CITIZEN)

    with pytest.raises(AuthorizationError):
        service.update_status(
            1,
            citizen,
            ReportStatus.RESOLVED.value,
        )


# Valid status transition should succeed
def test_update_status_success():
    service = build_service()

    operator = make_user(
        id=10,
        role=Role.OPERATOR,
        category_id=1,
    )

    report = make_report(
        id=1,
        category_id=1,
        status=ReportStatus.ASSIGNED,
    )

    service.report_repository.get_by_id.return_value = report

    result = service.update_status(
        1,
        operator,
        ReportStatus.IN_PROGRESS.value,
    )

    assert result == report
    assert report.status == ReportStatus.IN_PROGRESS

    service.report_repository.add_status_entry.assert_called_once()
    service.notification_service.notify_status_change.assert_called_once()
    service.session.commit.assert_called_once()

# Reporter and followers should all receive notifications
def test_recipients_include_followers():
    report = Mock()

    reporter = make_user(id=1)

    follower = Mock()
    follower.user = make_user(id=2)

    report.reporter = reporter
    report.followers = [follower]

    recipients = ReportService._recipients(report)

    assert recipients == [reporter, follower.user]

# Rejected report should store rejection reason
def test_update_status_rejected_success():
    service = build_service()

    operator = make_user(
        id=10,
        role=Role.OPERATOR,
        category_id=1,
    )

    report = make_report(
        id=1,
        category_id=1,
        status=ReportStatus.PENDING_APPROVAL,
    )

    service.report_repository.get_by_id.return_value = report

    result = service.update_status(
        1,
        operator,
        ReportStatus.REJECTED.value,
        note="Duplicate report",
    )

    assert result == report
    assert report.status == ReportStatus.REJECTED
    assert report.rejection_reason == "Duplicate report"

    service.report_repository.add_status_entry.assert_called_once()
    service.notification_service.notify_status_change.assert_called_once()
    service.session.commit.assert_called_once()

# Operator with same category can access private report
def test_get_accessible_report_operator_same_category():
    service = build_service()

    report = make_report(
        reporter_id=1,
        category_id=5,
    )

    service.report_repository.get_by_id.return_value = report

    operator = make_user(
        id=99,
        role=Role.OPERATOR,
        category_id=5,
    )

    result = service.get_accessible_report(
        1,
        operator,
    )

    assert result == report