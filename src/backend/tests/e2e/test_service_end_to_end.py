from __future__ import annotations

import pytest

from participium import create_app
from participium.database import close_connection, get_session
from participium.models.category import Category


@pytest.mark.e2e
def test_register_verify_and_login_flow(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    monkeypatch.setenv("AUTO_INIT_DB", "true")
    monkeypatch.setenv("BOOTSTRAP_REFERENCE_DATA", "false")
    monkeypatch.setenv("BOOTSTRAP_DEMO_DATA", "false")
    monkeypatch.setenv("EXPOSE_VERIFICATION_LINKS", "true")

    application = create_app()
    application.config.update(TESTING=True)
    client = application.test_client()

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


@pytest.mark.e2e
def test_categories_endpoint_returns_active_category(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    monkeypatch.setenv("AUTO_INIT_DB", "true")
    monkeypatch.setenv("BOOTSTRAP_REFERENCE_DATA", "false")
    monkeypatch.setenv("BOOTSTRAP_DEMO_DATA", "false")

    application = create_app()
    application.config.update(TESTING=True)
    client = application.test_client()

    with application.app_context():
        session = get_session()
        session.add(Category(name="E2E Category", is_active=True))
        session.commit()

    response = client.get("/api/v1/categories")
    assert response.status_code == 200
    assert any(item["name"] == "E2E Category" for item in response.get_json())

    close_connection()
    

    @pytest.mark.e2e
def test_create_and_fetch_public_report(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    monkeypatch.setenv("AUTO_INIT_DB", "true")
    monkeypatch.setenv("BOOTSTRAP_REFERENCE_DATA", "false")
    monkeypatch.setenv("BOOTSTRAP_DEMO_DATA", "false")
    monkeypatch.setenv("EXPOSE_VERIFICATION_LINKS", "true")

    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()

    # register / verify / login so the client is authenticated
    user = {
        "username": "reporter",
        "first_name": "Rep",
        "last_name": "Orter",
        "email": "reporter@example.com",
        "password": "Pass1234",
    }
    reg = client.post("/api/v1/auth/register", json=user)
    assert reg.status_code == 201
    ver_url = reg.get_json().get("verification_url")
    assert ver_url
    token = ver_url.rsplit("/", 1)[-1]
    verify_resp = client.get(f"/api/v1/auth/verify/{token}")
    assert verify_resp.status_code == 200
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"identifier": user["username"], "password": user["password"]},
    )
    assert login_resp.status_code == 200

    with app.app_context():
        session = get_session()
        session.add(Category(name="PublicCat", is_active=True))
        session.commit()

    report_payload = {
        "title": "E2E report",
        "description": "Tiny E2E",
        "latitude": 45.0,
        "longitude": 7.0,
        "category": "PublicCat",
    }

    resp = client.post("/api/v1/reports", json=report_payload)

    if resp.status_code in (200, 201):
        body = resp.get_json()
        assert body and ("id" in body or "report" in body)
        list_resp = client.get("/api/v1/reports")
        assert list_resp.status_code == 200
        titles = [r.get("title") for r in list_resp.get_json()]
        assert "E2E report" in titles
    else:
        assert resp.status_code == 400
        list_resp = client.get("/api/v1/reports")
        assert list_resp.status_code == 200

    close_connection()
