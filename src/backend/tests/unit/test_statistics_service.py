from datetime import datetime
from unittest.mock import Mock

from participium.services.statistics_service import StatisticsService
from participium.models.report import Report
from participium.models.user import User
from participium.models.category import Category
from participium.models.enums import ReportStatus, Role


# Build StatisticsService with mocked repository
def build_service():
    return StatisticsService(
        report_repository=Mock(),
    )


# Create a test user
def make_user(id=1, username="user"):
    user = User(
        username=username,
        first_name="Test",
        last_name="User",
        email=f"{username}@test.com",
        password_hash="hash",
        role=Role.CITIZEN,
    )
    user.id = id
    return user


# Create a test category
def make_category(name="Roads"):
    category = Category(
        name=name,
        is_active=True,
    )
    category.id = 1
    return category


# Create a test report
def make_report(
    category_name="Roads",
    status=ReportStatus.RESOLVED,
    created_at=None,
    reporter=None,
):
    report = Report(
        title="Title",
        description="Description",
        latitude=45.0,
        longitude=7.0,
        category_id=1,
    )

    report.category = make_category(category_name)
    report.status = status
    report.created_at = created_at or datetime(
        2025,
        1,
        1,
    )
    report.reporter = reporter

    return report


# Daily aggregation should group by day
def test_public_statistics_day():
    service = build_service()

    reports = [
        make_report(
            created_at=datetime(2025, 1, 1),
        ),
        make_report(
            created_at=datetime(2025, 1, 1),
        ),
        make_report(
            created_at=datetime(2025, 1, 2),
        ),
    ]

    service.report_repository.list_reports.return_value = reports

    result = service.public_statistics()

    assert result["total_reports"] == 3
    assert result["reports_by_category"]["Roads"] == 3

    assert result["trends"] == {
        "2025-01-01": 2,
        "2025-01-02": 1,
    }


# Weekly aggregation should use ISO weeks
def test_public_statistics_week():
    service = build_service()

    reports = [
        make_report(
            created_at=datetime(2025, 1, 1),
        ),
        make_report(
            created_at=datetime(2025, 1, 2),
        ),
    ]

    service.report_repository.list_reports.return_value = reports

    result = service.public_statistics(
        granularity="week",
    )

    assert len(result["trends"]) == 1


# Monthly aggregation should group by month
def test_public_statistics_month():
    service = build_service()

    reports = [
        make_report(
            created_at=datetime(2025, 1, 1),
        ),
        make_report(
            created_at=datetime(2025, 1, 20),
        ),
        make_report(
            created_at=datetime(2025, 2, 1),
        ),
    ]

    service.report_repository.list_reports.return_value = reports

    result = service.public_statistics(
        granularity="month",
    )

    assert result["trends"] == {
        "2025-01": 2,
        "2025-02": 1,
    }


# Admin statistics should generate all counters
def test_admin_statistics():
    service = build_service()

    reporter = make_user(
        id=1,
        username="john",
    )

    reports = [
        make_report(
            category_name="Roads",
            status=ReportStatus.RESOLVED,
            reporter=reporter,
        ),
        make_report(
            category_name="Roads",
            status=ReportStatus.RESOLVED,
            reporter=reporter,
        ),
        make_report(
            category_name="Lighting",
            status=ReportStatus.PENDING_APPROVAL,
            reporter=reporter,
        ),
    ]

    service.report_repository.list_all.return_value = reports

    result = service.admin_statistics()

    assert result["reports_by_status"]["Resolved"] == 2
    assert result["reports_by_status"]["Pending Approval"] == 1

    assert result["reports_by_type"]["Roads"] == 2
    assert result["reports_by_type"]["Lighting"] == 1

    assert result["top_1_percent_by_type"]
    assert result["top_5_percent_by_type"]


# Deleted reporter label branch
def test_reporter_label_deleted_user():
    report = make_report(
        reporter=None,
    )

    label = StatisticsService._reporter_label(
        report,
    )

    assert label == "Deleted Citizen"


# Existing reporter label branch
def test_reporter_label_normal_user():
    reporter = make_user(
        id=99,
        username="alice",
    )

    report = make_report(
        reporter=reporter,
    )

    label = StatisticsService._reporter_label(
        report,
    )

    assert label == "alice (99)"


# Empty reports should return empty breakdown
def test_top_percent_breakdown_empty():
    service = build_service()

    result = service._top_percent_breakdown(
        [],
        1,
    )

    assert result == {}


# Top reporter categories should be counted
def test_top_percent_breakdown_returns_categories():
    service = build_service()

    top_user = make_user(
        id=1,
        username="top",
    )

    other_user = make_user(
        id=2,
        username="other",
    )

    reports = [
        make_report(
            category_name="Roads",
            reporter=top_user,
        ),
        make_report(
            category_name="Roads",
            reporter=top_user,
        ),
        make_report(
            category_name="Lighting",
            reporter=other_user,
        ),
    ]

    result = service._top_percent_breakdown(
        reports,
        100,
    )

    assert result["Roads"] == 2
    assert result["Lighting"] == 1