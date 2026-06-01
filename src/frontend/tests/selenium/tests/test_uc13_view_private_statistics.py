from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.auth_page import login


def test_uc13_view_private_statistics_as_admin(driver, frontend_url):
    """UC-13: View private statistics - admin can access private statistics panel."""
    wait = WebDriverWait(driver, 15)

    # Login as admin; seeded credentials exist in backend
    login(driver, frontend_url, identifier="admin@example.com", password="Admin123!")

    # Admin page should load and show statistics section
    wait.until(EC.presence_of_element_located((By.ID, "admin-statistics-title")))
    assert "Statistics" in driver.find_element(By.ID, "admin-statistics-title").text
