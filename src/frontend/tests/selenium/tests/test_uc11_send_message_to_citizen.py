import time
import os
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.auth_page import login


def ensure_assigned_report(backend_api: str):
    # reuse pattern from other tests: create report and assign
    s_op = requests.Session()
    op_login = s_op.post(f"{backend_api}/auth/login", json={"identifier": "operator@example.com", "password": "Operator123!"})
    if op_login.status_code != 200:
        raise AssertionError(f"Operator API login failed: {op_login.status_code} {op_login.text}")
    op_profile = s_op.get(f"{backend_api}/users/me").json()
    operator_category_id = op_profile.get("category_id")
    if not operator_category_id:
        raise AssertionError("Operator has no category assigned; cannot create report")

    c = requests.Session()
    login_resp = c.post(f"{backend_api}/auth/login", json={"identifier": "citizen@example.com", "password": "Citizen123!"})
    if login_resp.status_code != 200:
        raise AssertionError(f"Citizen API login failed: {login_resp.status_code} {login_resp.text}")

    asset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/test-photo.png"))
    unique = str(int(time.time() * 1000))
    title = f"Selenium message report {unique}"
    with open(asset_path, "rb") as f:
        files = [("photos", (os.path.basename(asset_path), f, "image/png"))]
        data = {
            "title": title,
            "description": "Auto-created report for UC-11 test",
            "category_id": str(operator_category_id),
            "latitude": "45.070300",
            "longitude": "7.686850",
            "is_anonymous": "false",
        }
        resp = c.post(f"{backend_api}/reports", data=data, files=files)
    if resp.status_code not in (200, 201):
        raise AssertionError(f"API create report failed: {resp.status_code} {resp.text}")
    report = resp.json()

    assign_resp = s_op.post(f"{backend_api}/operator/reports/{report.get('id')}/assign")
    if assign_resp.status_code not in (200, 201):
        raise AssertionError(f"Operator assign failed: {assign_resp.status_code} {assign_resp.text}")

    return report


def test_uc11_send_message_to_citizen(driver, frontend_url):
    """UC-11: Send message to Citizen - operator composes message from report detail."""
    wait = WebDriverWait(driver, 20)
    backend_api = "http://localhost:5050/api/v1"

    report = ensure_assigned_report(backend_api)
    report_id = report.get("id")

    # Login as operator via UI
    login(driver, frontend_url, identifier="operator@example.com", password="Operator123!")

    # Open operator page and click the assigned report detail link
    driver.get(f"{frontend_url}/operator")
    open_link_id = f"assigned-report-row-{report_id}-open-detail"
    wait.until(EC.element_to_be_clickable((By.ID, open_link_id))).click()

    # On report detail, send a message
    wait.until(EC.presence_of_element_located((By.ID, "report-message-body")))
    body = f"Automated operator message {int(time.time())}"
    driver.find_element(By.ID, "report-message-body").send_keys(body)
    driver.find_element(By.ID, "report-message-submit").click()

    # Confirm the message appears in the conversation
    wait.until(
        lambda d:
        body in d.find_element(
            By.ID,
            "messages-list"
        ).text
    )
