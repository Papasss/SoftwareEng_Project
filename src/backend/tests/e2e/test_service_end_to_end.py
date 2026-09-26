from __future__ import annotations

from io import BytesIO
from typing import Any

import pytest
from sqlalchemy import select

from participium import create_app
from participium.database import close_connection, get_session
from participium.models.category import Category
from participium.models.enums import ReportStatus, Role
from participium.models.report import Report
from participium.models.user import User


pytestmark = pytest.mark.e2e


def _make_app(monkeypatch: pytest.MonkeyPatch, *, expose_verification_links: bool = True):
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    monkeypatch.setenv("AUTO_INIT_DB", "true")
    monkeypatch.setenv("BOOTSTRAP_REFERENCE_DATA", "false")
    monkeypatch.setenv("BOOTSTRAP_DEMO_DATA", "false")
    monkeypatch.setenv("EXPOSE_VERIFICATION_LINKS", "true" if expose_verification_links else "false")

    application = create_app()
    application.config.update(TESTING=True)
    return application, application.test_client()


def _register_verify_login(client, payload: dict[str, str]) -> None:
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    body = response.get_json()
    verification_url = body["verification_url"]
    token = verification_url.rsplit("/", 1)[-1]
    verify_response = client.get(f"/api/v1/auth/verify/{token}")
    assert verify_response.status_code == 200
    login_response = client.post(
        "/api/v1/auth/login",
        json={"identifier": payload["username"], "password": payload["password"]},
    )
    assert login_response.status_code == 200


def _create_category(application, name: str, is_active: bool = True) -> Category:
    with application.app_context():
        session = get_session()
        category = Category(name=name, is_active=is_active)
        session.add(category)
        session.commit()
        session.refresh(category)
        return category


def _set_user_role(application, username: str, role: Role, category_id: int | None = None) -> User:
    with application.app_context():
        session = get_session()
        user = session.scalars(select(User).filter_by(username=username)).first()
        assert user is not None
        user.role = role
        user.category_id = category_id
        session.commit()
        return user


def _create_report(client, category_id: int, title: str, description: str) -> dict[str, Any]:
    response = client.post(
        "/api/v1/reports",
        data={
            "title": title,
            "description": description,
            "latitude": "45.0",
            "longitude": "7.0",
            "category_id": str(category_id),
            "is_anonymous": "false",
            "photos": (BytesIO(b"photo-bytes"), "photo.jpg"),
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 201
    return response.get_json()


def test_health_reference_data_and_not_found_are_served(monkeypatch: pytest.MonkeyPatch):
    application, client = _make_app(monkeypatch, expose_verification_links=False)

    health_response = client.get("/api/v1/health")
    assert health_response.status_code == 200

    reference_response = client.get("/api/v1/meta/reference-data")
    assert reference_response.status_code == 200
    reference_body = reference_response.get_json()
    assert "citizen" in reference_body["roles"]
    assert "Resolved" in reference_body["report_statuses"]

    with client.session_transaction() as session:
        session["user_id"] = 999999

    cleanup_response = client.get("/api/v1/health")
    assert cleanup_response.status_code == 200
    with client.session_transaction() as session:
        assert "user_id" not in session

    missing_response = client.get("/api/v1/does-not-exist")
    assert missing_response.status_code == 404
    assert missing_response.get_json()["error"] == "Resource not found."

    close_connection()


def test_categories_endpoint_returns_active_category(monkeypatch: pytest.MonkeyPatch):
    application, client = _make_app(monkeypatch, expose_verification_links=False)

    with application.app_context():
        session = get_session()
        session.add(Category(name="E2E Category", is_active=True))
        session.commit()

    response = client.get("/api/v1/categories")
    assert response.status_code == 200
    assert any(item["name"] == "E2E Category" for item in response.get_json())

    close_connection()


def test_create_and_fetch_public_report(monkeypatch: pytest.MonkeyPatch):
    app, client = _make_app(monkeypatch)

    reporter = {
        "username": "reporter",
        "first_name": "Rep",
        "last_name": "Orter",
        "email": "reporter@example.com",
        "password": "Pass1234",
    }
    _register_verify_login(client, reporter)

    category = _create_category(app, "PublicCat")
    report_body = _create_report(client, category.id, "E2E report", "Tiny E2E")
    report_id = report_body["id"]

    with app.app_context():
        session = get_session()
        persisted_report = session.get(Report, report_id)
        assert persisted_report is not None
        persisted_report.status = ReportStatus.RESOLVED
        session.commit()

    detail_resp = client.get(f"/api/v1/reports/{report_id}")
    assert detail_resp.status_code == 200
    assert detail_resp.get_json()["id"] == report_id

    public_reports_resp = client.get(f"/api/v1/reports?category_id={category.id}&status=Resolved&sort=asc")
    assert public_reports_resp.status_code == 200
    assert any(item["id"] == report_id for item in public_reports_resp.get_json())

    invalid_status_resp = client.get("/api/v1/reports?status=bogus")
    assert invalid_status_resp.status_code == 400

    export_resp = client.get(f"/api/v1/reports/export?category_id={category.id}&status=Resolved&sort=asc")
    assert export_resp.status_code == 200
    assert export_resp.mimetype == "text/csv"
    assert "E2E report" in export_resp.get_data(as_text=True)

    follow_resp = client.post(f"/api/v1/reports/{report_id}/follow")
    assert follow_resp.status_code == 200

    unfollow_resp = client.delete(f"/api/v1/reports/{report_id}/follow")
    assert unfollow_resp.status_code == 200

    messages_resp = client.get(f"/api/v1/reports/{report_id}/messages")
    assert messages_resp.status_code == 200
    assert messages_resp.get_json() == []

    stats_resp = client.get("/api/v1/stats/public?granularity=week")
    assert stats_resp.status_code == 200
    assert stats_resp.get_json()["total_reports"] >= 1

    my_reports_resp = client.get("/api/v1/users/me/reports")
    assert my_reports_resp.status_code == 200
    assert any(item["id"] == report_id for item in my_reports_resp.get_json())

    close_connection()


def test_user_profile_notifications_and_account_deletion(monkeypatch: pytest.MonkeyPatch):
    app, client = _make_app(monkeypatch)

    user = {
        "username": "profileuser",
        "first_name": "Profile",
        "last_name": "User",
        "email": "profile@example.com",
        "password": "Test1234",
    }
    _register_verify_login(client, user)

    me_resp = client.get("/api/v1/users/me")
    assert me_resp.status_code == 200
    assert me_resp.get_json()["username"] == user["username"]

    update_resp = client.put(
        "/api/v1/users/me",
        data={
            "username": "updated-profileuser",
            "first_name": "Updated",
            "last_name": "User",
        },
        content_type="multipart/form-data",
    )
    assert update_resp.status_code == 200
    updated_body = update_resp.get_json()
    assert updated_body["username"] == "updated-profileuser"
    assert updated_body["first_name"] == "Updated"
    assert updated_body["email_notifications_enabled"] is False

    logout_resp = client.post("/api/v1/auth/logout")
    assert logout_resp.status_code == 200

    login_resp = client.post(
        "/api/v1/auth/login",
        json={"identifier": "updated-profileuser", "password": user["password"]},
    )
    assert login_resp.status_code == 200

    delete_resp = client.delete("/api/v1/users/me")
    assert delete_resp.status_code == 200

    after_delete_resp = client.get("/api/v1/users/me")
    assert after_delete_resp.status_code == 401

    close_connection()


def test_admin_and_operator_routes_cover_management_and_messages(monkeypatch: pytest.MonkeyPatch):
    app, client = _make_app(monkeypatch)

    admin_payload = {
        "username": "adminuser",
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@example.com",
        "password": "Admin1234",
    }
    reporter_payload = {
        "username": "citizenuser",
        "first_name": "Citizen",
        "last_name": "User",
        "email": "citizen@example.com",
        "password": "Citizen1234",
    }

    _register_verify_login(client, admin_payload)
    _set_user_role(app, admin_payload["username"], Role.ADMIN)
    admin_category = _create_category(app, "Admin Ops Category")

    client.post("/api/v1/auth/logout")
    _register_verify_login(client, reporter_payload)
    report_body = _create_report(client, admin_category.id, "Admin flow report", "Need attention")
    report_id = report_body["id"]

    client.post("/api/v1/auth/logout")
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"identifier": admin_payload["username"], "password": admin_payload["password"]},
    )
    assert login_resp.status_code == 200

    pending_resp = client.get("/api/v1/operator/reports/pending")
    assert pending_resp.status_code == 200

    assigned_resp = client.get("/api/v1/operator/reports/assigned")
    assert assigned_resp.status_code == 200

    assign_resp = client.post(f"/api/v1/operator/reports/{report_id}/assign")
    assert assign_resp.status_code == 200

    status_resp = client.post(
        f"/api/v1/operator/reports/{report_id}/status",
        json={"status": ReportStatus.RESOLVED.value, "note": "Resolved by test"},
    )
    assert status_resp.status_code == 200

    message_resp = client.post(
        f"/api/v1/reports/{report_id}/messages",
        json={"body": "Status updated in test"},
    )
    assert message_resp.status_code == 201

    thread_resp = client.get(f"/api/v1/reports/{report_id}/messages")
    assert thread_resp.status_code == 200
    assert thread_resp.get_json()

    users_before = client.get("/api/v1/admin/users")
    assert users_before.status_code == 200

    created_category_resp = client.post("/api/v1/admin/categories", json={"name": "Managed Category"})
    assert created_category_resp.status_code == 201
    created_category_id = created_category_resp.get_json()["id"]

    updated_category_resp = client.put(
        f"/api/v1/admin/categories/{admin_category.id}",
        json={"name": "Renamed Admin Ops Category", "is_active": False},
    )
    assert updated_category_resp.status_code == 200

    created_user_resp = client.post(
        "/api/v1/admin/users",
        json={
            "username": "managed-operator",
            "first_name": "Managed",
            "last_name": "Operator",
            "email": "managed-operator@example.com",
            "password": "Operator1234",
            "role": "operator",
            "category_id": str(created_category_id),
            "is_active": True,
            "email_notifications_enabled": False,
        },
    )
    assert created_user_resp.status_code == 201
    managed_user_id = created_user_resp.get_json()["id"]

    updated_user_resp = client.put(
        f"/api/v1/admin/users/{managed_user_id}",
        json={
            "username": "managed-operator-updated",
            "first_name": "Managed",
            "last_name": "Updated",
            "email": "managed-operator-updated@example.com",
            "role": "citizen",
            "is_active": False,
            "email_notifications_enabled": True,
        },
    )
    assert updated_user_resp.status_code == 200

    categories_resp = client.get("/api/v1/admin/categories")
    assert categories_resp.status_code == 200

    stats_resp = client.get("/api/v1/admin/stats")
    assert stats_resp.status_code == 200

    client.post("/api/v1/auth/logout")
    reporter_login_resp = client.post(
        "/api/v1/auth/login",
        json={"identifier": reporter_payload["username"], "password": reporter_payload["password"]},
    )
    assert reporter_login_resp.status_code == 200

    notifications_resp = client.get("/api/v1/users/me/notifications")
    assert notifications_resp.status_code == 200
    notifications_body = notifications_resp.get_json()
    assert notifications_body

    notification_id = notifications_body[0]["id"]
    read_resp = client.post(f"/api/v1/users/me/notifications/{notification_id}/read")
    assert read_resp.status_code == 200
    assert read_resp.get_json()["is_read"] is True

    close_connection()


def test_register_verify_and_login_flow(monkeypatch: pytest.MonkeyPatch):
    application, client = _make_app(monkeypatch)

    payload = {
        "username": "e2euser",
        "first_name": "E2E",
        "last_name": "Tester",
        "email": "e2euser@example.com",
        "password": "Test1234",
    }

    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    body = response.get_json()
    assert body["user"]["email"] == payload["email"]
    assert "verification_url" in body

    token = body["verification_url"].rsplit("/", 1)[-1]
    response = client.get(f"/api/v1/auth/verify/{token}")
    assert response.status_code == 200
    assert response.get_json()["user"]["is_email_verified"] is True

    login_response = client.post(
        "/api/v1/auth/login",
        json={"identifier": payload["username"], "password": payload["password"]},
    )
    assert login_response.status_code == 200
    assert login_response.get_json()["message"] == "Logged in."

    close_connection()


def test_verify_invalid_token_returns_error(monkeypatch: pytest.MonkeyPatch):
    application, client = _make_app(monkeypatch)

    resp = client.get("/api/v1/auth/verify/this-token-does-not-exist")
    assert resp.status_code in (400, 404, 410)

    close_connection()


def test_register_duplicate_user_returns_error(monkeypatch: pytest.MonkeyPatch):
    application, client = _make_app(monkeypatch)

    payload = {
        "username": "dupuser",
        "first_name": "D",
        "last_name": "Up",
        "email": "dup@example.com",
        "password": "Dup1234",
    }
    r1 = client.post("/api/v1/auth/register", json=payload)
    assert r1.status_code == 201
    r2 = client.post("/api/v1/auth/register", json=payload)
    assert r2.status_code in (400, 409)

    close_connection()


def test_post_report_requires_auth(monkeypatch: pytest.MonkeyPatch):
    application, client = _make_app(monkeypatch, expose_verification_links=False)

    with application.app_context():
        session = get_session()
        session.add(Category(name="AuthReqCat", is_active=True))
        session.commit()

    payload = {
        "title": "Auth required",
        "description": "Should require auth",
        "latitude": 0.0,
        "longitude": 0.0,
        "category": "AuthReqCat",
    }
    resp = client.post("/api/v1/reports", json=payload)
    assert resp.status_code in (400, 401)

    close_connection()


def test_get_reports_empty_list(monkeypatch: pytest.MonkeyPatch):
    application, client = _make_app(monkeypatch, expose_verification_links=False)

    resp = client.get("/api/v1/reports")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)

    close_connection()


def test_get_nonexistent_report_returns_404(monkeypatch: pytest.MonkeyPatch):
    application, client = _make_app(monkeypatch, expose_verification_links=False)

    resp = client.get("/api/v1/reports/999999999")
    assert resp.status_code in (400, 404)

    close_connection()
