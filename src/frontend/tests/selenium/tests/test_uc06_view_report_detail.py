import os
import time
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_public_report_if_needed(backend_api: str):
    s = requests.Session()
    # check existing public reports
    list_resp = s.get(f"{backend_api}/reports")
    if list_resp.status_code == 200 and list_resp.json():
        return list_resp.json()[0]

    # get operator category
    s_op = requests.Session()
    op_login = s_op.post(f"{backend_api}/auth/login", json={"identifier": "operator@example.com", "password": "Operator123!"})
    if op_login.status_code != 200:
        raise AssertionError(f"Operator API login failed: {op_login.status_code} {op_login.text}")
    op_profile = s_op.get(f"{backend_api}/users/me").json()
    operator_category_id = op_profile.get("category_id")
    if not operator_category_id:
        raise AssertionError("Operator has no category assigned; cannot create report")

    # create as citizen
    c = requests.Session()
    login_resp = c.post(f"{backend_api}/auth/login", json={"identifier": "citizen@example.com", "password": "Citizen123!"})
    if login_resp.status_code != 200:
        raise AssertionError(f"Citizen API login failed: {login_resp.status_code} {login_resp.text}")

    asset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/test-photo.png"))
    unique = str(int(time.time() * 1000))
    title = f"Selenium detail report {unique}"
    with open(asset_path, "rb") as f:
        files = [("photos", (os.path.basename(asset_path), f, "image/png"))]
        data = {
            "title": title,
            "description": "Auto-created report for UC-06 detail test",
            "category_id": str(operator_category_id),
            "latitude": "45.070300",
            "longitude": "7.686850",
            "is_anonymous": "false",
        }
        resp = c.post(f"{backend_api}/reports", data=data, files=files)
    if resp.status_code not in (200, 201):
        raise AssertionError(f"API create report failed: {resp.status_code} {resp.text}")
    report = resp.json()

    # assign using operator
    assign_resp = s_op.post(f"{backend_api}/operator/reports/{report.get('id')}/assign")
    if assign_resp.status_code not in (200, 201):
        raise AssertionError(f"Operator assign failed: {assign_resp.status_code} {assign_resp.text}")

    return report


def test_uc06_view_report_detail(driver, frontend_url):
    """UC-06: View report detail shows title, description, category, map, photos, and status."""
    wait = WebDriverWait(driver, 15)
    backend_api = "http://localhost:5050/api/v1"

    report = create_public_report_if_needed(backend_api)
    report_id = report.get("id")
    assert report_id, "Failed to obtain or create a public report"

    # Open the report detail page via the frontend
    driver.get(f"{frontend_url}/reports/{report_id}")
    wait.until(EC.presence_of_element_located((By.ID, "report-detail-title")))

    title = driver.find_element(By.ID, "report-detail-title").text
    assert title == report.get("title"), f"Title mismatch: page='{title}' vs api='{report.get('title')}'"

    description = driver.find_element(By.ID, "report-detail-description").text
    assert description == (report.get("description") or ""), "Description mismatch"

    category = driver.find_element(By.ID, "report-detail-category-value").text
    assert category == report.get("category", {}).get("name"), f"Category mismatch: {category} vs {report.get('category')}"

    status_text = driver.find_element(By.CSS_SELECTOR, "#report-detail-status").text
    assert report.get("status") in status_text, f"Status mismatch: '{status_text}' does not contain '{report.get('status')}'"

    # map presence
    assert driver.find_element(By.ID, "report-detail-map"), "Report map not present"

    # photos
    photos = report.get("photos", [])
    if photos:
        # at least one image should be visible in the photo grid
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#report-detail-photo-grid img")))
        imgs = driver.find_elements(By.CSS_SELECTOR, "#report-detail-photo-grid img")
        assert len(imgs) >= 1, "Expected at least one photo image on detail page"
    else:
        # no photos: ensure 'No photos' message exists
        assert driver.find_element(By.CSS_SELECTOR, "#report-detail-no-photos")
