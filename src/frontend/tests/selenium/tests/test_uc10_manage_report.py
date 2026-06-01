import time
import os
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.auth_page import login


def ensure_assignable_report(backend_api: str):
    s = requests.Session()
    # fetch operator category
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
    title = f"Selenium manage report {unique}"
    with open(asset_path, "rb") as f:
        files = [("photos", (os.path.basename(asset_path), f, "image/png"))]
        data = {
            "title": title,
            "description": "Auto-created report for UC-10 test",
            "category_id": str(operator_category_id),
            "latitude": "45.070300",
            "longitude": "7.686850",
            "is_anonymous": "false",
        }
        resp = c.post(f"{backend_api}/reports", data=data, files=files)
    if resp.status_code not in (200, 201):
        raise AssertionError(f"API create report failed: {resp.status_code} {resp.text}")
    report = resp.json()

    # assign using operator session to make it manageable
    assign_resp = s_op.post(f"{backend_api}/operator/reports/{report.get('id')}/assign")
    if assign_resp.status_code not in (200, 201):
        raise AssertionError(f"Operator assign failed: {assign_resp.status_code} {assign_resp.text}")

    return report


def test_uc10_manage_report_update_status(driver, frontend_url):
    """UC-10: Manage report - operator updates status and note."""
    wait = WebDriverWait(driver, 20)
    backend_api = "http://localhost:5050/api/v1"

    report = ensure_assignable_report(backend_api)
    report_id = report.get("id")
    assert report_id, "Failed to obtain or create report"

    # Login as operator via UI
    login(driver, frontend_url, identifier="operator@example.com", password="Operator123!")

    # Navigate to operator page and wait for assigned table
    driver.get(f"{frontend_url}/operator")
    row_id = f"assigned-report-row-{report_id}"
    wait.until(EC.presence_of_element_located((By.ID, row_id)))

    # Select a different status than current by choosing the first available option
    select_id = f"assigned-report-status-{report_id}"
    select = wait.until(EC.presence_of_element_located((By.ID, select_id)))
    options = select.find_elements(By.TAG_NAME, "option")
    assert options, "No status options available"
    current = select.get_attribute("value") or options[0].get_attribute("value")
    next_opt = None
    for opt in options:
        val = opt.get_attribute("value")
        if val and val != current:
            next_opt = val
            opt.click()
            break
    assert next_opt, "No alternative status option found"

    # Enter a note and click update
    note_input_id = f"assigned-report-note-{report_id}"
    note_input = driver.find_element(By.ID, note_input_id)
    note_input.clear()
    note_input.send_keys("Automated status update from Selenium test")

    update_btn_id = f"assigned-report-update-{report_id}"
    driver.find_element(By.ID, update_btn_id).click()

    # Verify via backend API that the status changed
    s = requests.Session()
    s.post(f"{backend_api}/auth/login", json={"identifier": "operator@example.com", "password": "Operator123!"})
    r = s.get(f"{backend_api}/reports/{report_id}")
    assert r.status_code == 200, f"Failed to fetch report after update: {r.status_code} {r.text}"
    assert r.json().get("status") == next_opt, f"Report status did not update: {r.json().get('status')} vs {next_opt}"
