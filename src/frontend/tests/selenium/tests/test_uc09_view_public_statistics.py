from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_uc09_view_public_statistics(driver, frontend_url):
    """UC-09: View public statistics - statistics panel is visible and shows totals."""
    wait = WebDriverWait(driver, 10)

    driver.get(frontend_url)
    wait.until(EC.presence_of_element_located((By.ID, "public-statistics-title")))
    total = driver.find_element(By.ID, "public-total-reports-value").text.strip()
    # total should be present and parseable as integer (0+)
    assert total.isdigit(), f"Public total reports value not numeric: {total}"
