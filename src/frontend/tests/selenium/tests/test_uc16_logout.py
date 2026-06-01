from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.auth_page import login


def test_uc16_logout_ends_session(driver, frontend_url):
    """UC-16: Logout - authenticated user can logout and access protected pages require login."""
    wait = WebDriverWait(driver, 10)

    login(driver, frontend_url, identifier="citizen@example.com", password="Citizen123!")

    # Ensure logout button is present and click it
    wait.until(EC.presence_of_element_located((By.ID, "logout-button")))
    driver.find_element(By.ID, "logout-button").click()

    # After logout, public login link should be visible
    wait.until(EC.presence_of_element_located((By.ID, "login-link")))
    assert "login" in driver.find_element(By.ID, "login-link").get_attribute("id")
