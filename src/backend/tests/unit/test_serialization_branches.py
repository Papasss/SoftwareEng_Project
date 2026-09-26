from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from participium.core import serialization
from participium.core.utils import build_csv, parse_date
from participium.models.enums import Role, ReportStatus
from participium.models.report import Report, ReportPhoto, ReportStatusHistory, ReportFollower
from participium.models.category import Category
from participium.models.user import User


def make_user(id=1, role=Role.CITIZEN):
    u = User(username="u", first_name="F", last_name="L", email="e@x.com", password_hash="p", role=role)
    u.id = id
    u.created_at = datetime.utcnow()
    return u


def test_serialize_party_deleted_user():
    party = serialization._serialize_party(None)
    assert party["id"] is None and "Deleted" in party["display_name"]


def test_serialize_reporter_anonymous_and_viewer_none():
    reporter = make_user(id=10)
    report = Report(title="t", description="d", latitude=0.0, longitude=0.0, category_id=1)
    report.reporter = reporter
    report.reporter_id = 10
    report.is_anonymous = True

    out = serialization._serialize_reporter(report, viewer=None)
    assert out["id"] is None and "Anonymous" in out["display_name"]


def test_serialize_reporter_anonymous_admin_sees():
    reporter = make_user(id=11)
    report = Report(title="t", description="d", latitude=0.0, longitude=0.0, category_id=2)
    report.reporter = reporter
    report.reporter_id = 11
    report.is_anonymous = True

    admin = make_user(id=99, role=Role.ADMIN)
    out = serialization._serialize_reporter(report, viewer=admin)
    assert out["id"] == reporter.id


def test_viewer_follows_report():
    user = make_user(id=5)
    report = Report(title="t", description="d", latitude=0, longitude=0, category_id=1)
    follower = ReportFollower()
    follower.user_id = 5
    report.followers = [follower]
    assert serialization._viewer_follows_report(report, user) is True
    assert serialization._viewer_follows_report(report, None) is False


def test_serialize_photo_and_media_url_none():
    p = ReportPhoto(file_path=None, original_filename="f")
    p.id = 3
    out = serialization.serialize_photo(p)
    assert out["id"] == 3 and out["url"] is None


def test_serialize_report_detail_includes_messages_and_history_ordering():
    reporter = make_user(id=7)
    report = Report(title="t", description="d", latitude=0, longitude=0, category_id=1)
    report.id = 77
    report.reporter = reporter
    report.reporter_id = reporter.id

    # status history with different created_at
    h1 = ReportStatusHistory()
    h1.id = 1
    h1.previous_status = ReportStatus.PENDING_APPROVAL
    h1.new_status = ReportStatus.ASSIGNED
    h1.note = "n1"
    h1.created_at = datetime.utcnow() - timedelta(days=1)

    h2 = ReportStatusHistory()
    h2.id = 2
    h2.previous_status = ReportStatus.ASSIGNED
    h2.new_status = ReportStatus.RESOLVED
    h2.note = "n2"
    h2.created_at = datetime.utcnow()

    report.status_history = [h2, h1]
    report.messages = []
    # attach a minimal category required by serializer
    cat = Category(name="c")
    cat.id = 1
    cat.created_at = datetime.utcnow()
    report.category = cat
    report.status = ReportStatus.ASSIGNED

    data = serialization.serialize_report_detail(report, viewer=reporter, include_messages=True)
    # history should be sorted by created_at
    assert data["status_history"][0]["id"] == 1


def test_parse_date_and_build_csv_cover_utility_branches():
    parsed = parse_date("2026-06-02T12:34:56")
    assert parsed.year == 2026
    assert parsed.month == 6
    assert parse_date(None) is None

    with pytest.raises(ValueError):
        parse_date("not-a-date")

    csv_text = build_csv(
        [{"id": 1, "title": "Example"}],
        ["id", "title"],
    )

    assert "id,title" in csv_text
    assert "1,Example" in csv_text
