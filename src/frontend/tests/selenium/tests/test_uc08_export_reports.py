from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_uc08_export_reports_link_present(driver, frontend_url):
    """UC-08: Export reports (CSV) - ensure export link is present and points to export endpoint."""
    wait = WebDriverWait(driver, 10)

    driver.get(frontend_url)
    # Wait for the Home page and the export link
    wait.until(EC.presence_of_element_located((By.ID, "public-export-link")))
    link = driver.find_element(By.ID, "public-export-link")
    href = link.get_attribute("href")
    assert href and "/reports/export" in href, f"Export link href looks incorrect: {href}"
