import os
import time
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def ensure_min_reports(backend_api: str, min_count: int = 2):
    s = requests.Session()

    op_login = s.post(
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

    profile = s.get(f"{backend_api}/users/me").json()

    category_id = profile.get("category_id")

    if not category_id:
        raise AssertionError(
            "Operator has no category assigned; "
            "cannot create reports"
        )

    list_resp = s.get(f"{backend_api}/reports")

    if list_resp.status_code != 200:
        raise AssertionError(
            f"Failed to list reports: "
            f"{list_resp.status_code} {list_resp.text}"
        )

    reports = list_resp.json()

    to_create = max(
        0,
        min_count - len(reports)
    )

    if to_create == 0:
        return

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

    for i in range(to_create):
        unique = str(int(time.time() * 1000)) + str(i)

        title = f"Selenium filter report {unique}"

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
                "description": "Auto-created for UC-05 test",
                "category_id": str(category_id),
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

        report_id = report.get("id")

        if not report_id:
            raise AssertionError(
                f"No report id returned: {report}"
            )

        assign_resp = s.post(
            f"{backend_api}/operator/reports/{report_id}/assign"
        )

        if assign_resp.status_code not in (200, 201):
            raise AssertionError(
                f"Operator assign failed: "
                f"{assign_resp.status_code} "
                f"{assign_resp.text}"
            )

        time.sleep(0.5)

    for _ in range(12):
        list_resp = s.get(f"{backend_api}/reports")

        if list_resp.status_code == 200:
            reports = list_resp.json()

            if len(reports) >= min_count:
                return

        time.sleep(1)

    raise AssertionError(
        f"Expected at least {min_count} public reports, "
        f"but backend did not reach that count in time"
    )


def test_uc05_search_filter_reports(driver, frontend_url):
    """UC-05: Search and filter reports in the public table."""

    wait = WebDriverWait(driver, 15)

    backend_api = "http://localhost:5050/api/v1"

    ensure_min_reports(
        backend_api,
        min_count=2
    )

    driver.get(frontend_url)

    wait.until(
        EC.presence_of_element_located(
            (By.ID, "public-report-table-body")
        )
    )

    wait.until(
        lambda d: len(
            d.find_elements(
                By.CSS_SELECTOR,
                "#public-report-table-body tr"
            )
        ) > 0
    )

    def read_titles():
        rows = driver.find_elements(
            By.CSS_SELECTOR,
            "#public-report-table-body tr"
        )

        titles = []

        for r in rows:
            rid = r.get_attribute("id")

            if not rid:
                continue

            try:
                titles.append(
                    driver.find_element(
                        By.ID,
                        f"{rid}-title"
                    ).text
                )
            except Exception:
                continue

        return titles

    titles_before = read_titles()

    assert len(titles_before) > 0, (
        "No public reports available to test filters"
    )

    first_row = driver.find_element(
        By.CSS_SELECTOR,
        "#public-report-table-body tr"
    )

    row_id = first_row.get_attribute("id")

    assert row_id

    category_text = driver.find_element(
        By.ID,
        f"{row_id}-category"
    ).text

    status_text = driver.find_element(
        By.ID,
        f"{row_id}-status"
    ).text

    category_select = driver.find_element(
        By.ID,
        "public-filter-category"
    )

    for opt in category_select.find_elements(
        By.TAG_NAME,
        "option"
    ):
        if opt.text.strip() == category_text.strip():
            opt.click()
            break

    driver.find_element(
        By.ID,
        "public-filter-submit"
    ).click()

    wait.until(
        lambda d: all(
            c.text.strip() == category_text.strip()
            for c in d.find_elements(
                By.CSS_SELECTOR,
                "#public-report-table-body td[id$='-category']"
            )
        )
    )

    cats = [
        c.text
        for c in driver.find_elements(
            By.CSS_SELECTOR,
            "#public-report-table-body td[id$='-category']"
        )
    ]

    assert all(
        ct.strip() == category_text.strip()
        for ct in cats
    ), (
        f"Not all rows match category "
        f"{category_text}: {cats}"
    )

    status_select = driver.find_element(
        By.ID,
        "public-filter-status"
    )

    for opt in status_select.find_elements(
        By.TAG_NAME,
        "option"
    ):
        if opt.text.strip() == status_text.strip():
            opt.click()
            break

    driver.find_element(
        By.ID,
        "public-filter-submit"
    ).click()

    wait.until(
        lambda d: all(
            s.text.strip() == status_text.strip()
            for s in d.find_elements(
                By.CSS_SELECTOR,
                "#public-report-table-body td[id$='-status']"
            )
        )
    )

    statuses = [
        s.text
        for s in driver.find_elements(
            By.CSS_SELECTOR,
            "#public-report-table-body td[id$='-status']"
        )
    ]

    assert all(
        st.strip() == status_text.strip()
        for st in statuses
    ), (
        f"Not all rows match status "
        f"{status_text}: {statuses}"
    )

    sort_select = driver.find_element(
        By.ID,
        "public-filter-sort"
    )

    sort_select.find_element(
        By.CSS_SELECTOR,
        "option[value='asc']"
    ).click()

    driver.find_element(
        By.ID,
        "public-filter-submit"
    ).click()

    time.sleep(0.5)

    titles_after = read_titles()

    if len(titles_before) > 1 and len(titles_after) > 0:
        assert (
            titles_before[0] != titles_after[0]
            or titles_before != titles_after
        ), "Sorting did not change the result order"