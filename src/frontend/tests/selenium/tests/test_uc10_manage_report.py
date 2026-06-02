import time
import os
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.auth_page import login


def ensure_assignable_report(backend_api: str):
    s_op = requests.Session()

    op_login = s_op.post(
        f"{backend_api}/auth/login",
        json={
            "identifier": "operator@example.com",
            "password": "Operator123!"
        }
    )

    if op_login.status_code != 200:
        raise AssertionError(
            f"Operator API login failed: "
            f"{op_login.status_code} {op_login.text}"
        )

    op_profile = s_op.get(
        f"{backend_api}/users/me"
    ).json()

    operator_category_id = op_profile.get(
        "category_id"
    )

    if not operator_category_id:
        raise AssertionError(
            "Operator has no category assigned; "
            "cannot create report"
        )

    c = requests.Session()

    login_resp = c.post(
        f"{backend_api}/auth/login",
        json={
            "identifier": "citizen@example.com",
            "password": "Citizen123!"
        }
    )

    if login_resp.status_code != 200:
        raise AssertionError(
            f"Citizen API login failed: "
            f"{login_resp.status_code} {login_resp.text}"
        )

    asset_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../assets/test-photo.png"
        )
    )

    unique = str(int(time.time() * 1000))

    title = f"Selenium manage report {unique}"

    with open(asset_path, "rb") as f:
        files = [
            (
                "photos",
                (
                    os.path.basename(asset_path),
                    f,
                    "image/png"
                )
            )
        ]

        data = {
            "title": title,
            "description": "Auto-created report for UC-10 test",
            "category_id": str(operator_category_id),
            "latitude": "45.070300",
            "longitude": "7.686850",
            "is_anonymous": "false",
        }

        resp = c.post(
            f"{backend_api}/reports",
            data=data,
            files=files
        )

    if resp.status_code not in (200, 201):
        raise AssertionError(
            f"API create report failed: "
            f"{resp.status_code} {resp.text}"
        )

    report = resp.json()

    assign_resp = s_op.post(
        f"{backend_api}/operator/reports/{report.get('id')}/assign"
    )

    if assign_resp.status_code not in (200, 201):
        raise AssertionError(
            f"Operator assign failed: "
            f"{assign_resp.status_code} "
            f"{assign_resp.text}"
        )

    return report


def test_uc10_manage_report_update_status(driver, frontend_url):
    wait = WebDriverWait(driver, 20)

    backend_api = "http://localhost:5050/api/v1"

    report = ensure_assignable_report(
        backend_api
    )

    report_id = report.get("id")

    login(
        driver,
        frontend_url,
        identifier="operator@example.com",
        password="Operator123!"
    )

    driver.get(f"{frontend_url}/operator")

    row_id = f"assigned-report-row-{report_id}"

    wait.until(
        EC.presence_of_element_located(
            (By.ID, row_id)
        )
    )

    select_id = f"assigned-report-status-{report_id}"

    select = wait.until(
        EC.presence_of_element_located(
            (By.ID, select_id)
        )
    )

    options = select.find_elements(
        By.TAG_NAME,
        "option"
    )

    current = (
        select.get_attribute("value")
        or options[0].get_attribute("value")
    )

    next_opt = None
    for opt in options:
        val = opt.get_attribute("value")

        if val and val != current:
            next_opt = val
            driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, select, val)

            time.sleep(1)

            break


    note_input_id = (
        f"assigned-report-note-{report_id}"
    )

    note_input = driver.find_element(
        By.ID,
        note_input_id
    )

    note_input.clear()

    note_input.send_keys(
        "Automated status update from Selenium test"
    )

    update_btn_id = (
        f"assigned-report-update-{report_id}"
    )

    driver.find_element(
        By.ID,
        update_btn_id
    ).click()

    s = requests.Session()

    s.post(
        f"{backend_api}/auth/login",
        json={
            "identifier": "operator@example.com",
            "password": "Operator123!"
        }
    )

    updated = False

    for _ in range(10):
        r = s.get(
            f"{backend_api}/reports/{report_id}"
        )

        if (
                r.status_code == 200
                and r.json().get("status") == next_opt
        ):
            updated = True
            break

        time.sleep(1)

    assert updated, (
        f"Report status did not update: "
        f"{r.json().get('status')} vs {next_opt}"
    )