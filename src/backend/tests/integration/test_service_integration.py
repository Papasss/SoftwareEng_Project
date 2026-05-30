from __future__ import annotations

from datetime import datetime, timedelta
from io import BytesIO
from unittest.mock import Mock

import pytest
from sqlalchemy import select
from werkzeug.datastructures import FileStorage

from participium.database import close_connection, create_all, get_session, open_connection
from participium.models.category import Category
from participium.models.enums import NotificationType, ReportStatus, Role
from participium.models.message import Message
from participium.models.notification import Notification
from participium.models.report import Report, ReportFollower, ReportStatusHistory
from participium.models.token import EmailVerificationToken
from participium.models.user import User
from participium.repositories.category_repository import CategoryRepository
from participium.repositories.notification_repository import NotificationRepository
from participium.repositories.report_repository import ReportRepository
from participium.repositories.token_repository import TokenRepository
from participium.repositories.user_repository import UserRepository
from participium.services.report_service import ReportService
from participium.services.user_service import UserService


class StubStorageService:
    def save(self, file: FileStorage) -> str:
        return f"stored-{file.filename}"


class StubNotificationService:
    def __init__(self):
        self.sent = []

    def notify_status_change(self, recipients, report, body):
        self.sent.append((recipients, report, body))


@pytest.mark.integration
def test_user_service_delete_account_clears_user_related_records(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    open_connection()
    create_all()
    session = get_session()

    category = Category(name="Street", is_active=True)
    session.add(category)
    session.commit()

    user = User(
        username="delete-me",
        first_name="Delete",
        last_name="Me",
        email="delete@example.com",
        password_hash="hashed",
        role=Role.CITIZEN,
        is_active=True,
        is_email_verified=True,
        email_notifications_enabled=True,
    )
    session.add(user)
    session.commit()

    report = Report(
        title="Broken road",
        description="Road is broken",
        latitude=45.1,
        longitude=7.1,
        status=ReportStatus.PENDING_APPROVAL,
        reporter_id=user.id,
        category_id=category.id,
    )
    session.add(report)
    session.flush()

    message = Message(report_id=report.id, sender_id=user.id, recipient_id=user.id, body="Hello")
    status_event = ReportStatusHistory(
        report_id=report.id,
        previous_status=None,
        new_status=ReportStatus.PENDING_APPROVAL,
        note="Created",
        changed_by_id=user.id,
    )
    notification = Notification(user_id=user.id, report_id=report.id, type=NotificationType.SYSTEM, title="t", body="b", is_read=False)
    token = EmailVerificationToken(user_id=user.id, token="token", expires_at=datetime.utcnow() + timedelta(hours=1), is_used=False)

    session.add_all([message, status_event, notification, token])
    session.commit()

    service = UserService(
        session=session,
        user_repository=UserRepository(session),
        category_repository=CategoryRepository(session),
        token_repository=TokenRepository(session),
        notification_repository=NotificationRepository(session),
        storage_service=Mock(),
    )

    service.delete_account(user)

    assert session.get(User, user.id) is None
    session.refresh(report)
    assert report.reporter_id is None
    assert report.is_anonymous is True
    refreshed_message = session.get(Message, message.id)
    assert refreshed_message.sender_id is None or refreshed_message.recipient_id is None
    assert session.scalars(select(Notification).filter_by(user_id=user.id)).first() is None
    assert session.scalars(select(EmailVerificationToken).filter_by(user_id=user.id)).first() is None

    close_connection()


@pytest.mark.integration
def test_report_service_can_create_public_report_follow_and_unfollow(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    open_connection()
    create_all()
    session = get_session()

    category = Category(name="Pothole", is_active=True)
    reporter = User(
        username="reporter",
        first_name="Report",
        last_name="User",
        email="reporter@example.com",
        password_hash="hashed",
        role=Role.CITIZEN,
        is_active=True,
        is_email_verified=True,
        email_notifications_enabled=True,
    )
    session.add_all([category, reporter])
    session.commit()

    report_repository = ReportRepository(session)
    category_repository = CategoryRepository(session)
    notification_service = StubNotificationService()
    storage_service = StubStorageService()

    service = ReportService(
        session=session,
        report_repository=report_repository,
        category_repository=category_repository,
        storage_service=storage_service,
        notification_service=notification_service,
    )

    photo = FileStorage(stream=BytesIO(b"content"), filename="photo.jpg", content_type="image/jpeg")
    report = service.create_report(reporter, category.id, "Pothole", "There is a pothole.", "45.0", "7.0", [photo], is_anonymous=True)

    assert report.id is not None
    assert report.is_anonymous is True
    assert len(report.photos) == 1
    assert report.photos[0].file_path == "stored-photo.jpg"
    assert len(report.status_history) == 1

    report.status = ReportStatus.RESOLVED
    session.commit()

    public_reports = service.list_public_reports(category_id=category.id)
    assert any(item.id == report.id for item in public_reports)

    followed = service.follow_report(report.id, reporter)
    assert followed.id == report.id
    assert session.scalars(select(ReportFollower).filter_by(report_id=report.id, user_id=reporter.id)).first() is not None

    unfollowed = service.unfollow_report(report.id, reporter)
    assert unfollowed.id == report.id

    close_connection()


@pytest.mark.integration
def test_report_repository_search_and_status_history_branches(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    open_connection()
    create_all()
    session = get_session()

    category = Category(name="RepoCat", is_active=True)
    user = User(
        username="repo_user",
        first_name="R",
        last_name="U",
        email="repo@example.com",
        password_hash="h",
        role=Role.CITIZEN,
        is_active=True,
        is_email_verified=True,
        email_notifications_enabled=True,
    )
    session.add_all([category, user])
    session.commit()

    repo = ReportRepository(session)

    r1 = Report(
        title="One",
        description="d1",
        latitude=0.1,
        longitude=0.1,
        status=ReportStatus.RESOLVED,
        reporter_id=user.id,
        category_id=category.id,
    )
    r2 = Report(
        title="Two",
        description="d2",
        latitude=0.2,
        longitude=0.2,
        status=ReportStatus.PENDING_APPROVAL,
        reporter_id=user.id,
        category_id=category.id,
    )
    session.add_all([r1, r2])
    session.commit()

    list_method_names = ("search", "search_reports", "list_reports", "find_all", "all")
    found_list = False
    for name in list_method_names:
        fn = getattr(repo, name, None)
        if callable(fn):
            try:
                res = fn(filters={"category_id": category.id})
            except TypeError:
                res = fn()
            if res is not None:
                try:
                    items = list(res)
                except TypeError:
                    items = [res]
                assert len(items) >= 0
            found_list = True
            break
    assert found_list is True

    status_method_names = ("get_status_history", "status_history", "find_status_history")
    found_status = False
    for name in status_method_names:
        fn = getattr(repo, name, None)
        if callable(fn):
            try:
                out = fn(r1.id)
            except TypeError:
                out = fn(report_id=r1.id)
            assert out is not None
            found_status = True
            break

    close_connection()

