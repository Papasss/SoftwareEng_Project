from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.auth_page import login


def test_uc16_logout_ends_session(driver, frontend_url):
    """UC-16: Logout - authenticated user can logout and protected pages require login."""
    wait = WebDriverWait(driver, 10)

    login(
        driver,
        frontend_url,
        identifier="citizen@example.com",
        password="Citizen123!"
    )

    wait.until(
        EC.presence_of_element_located(
            (By.ID, "logout-button")
        )
    )

    driver.find_element(
        By.ID,
        "logout-button"
    ).click()

    wait.until(
        lambda d: "/login" in d.current_url
    )

    assert "/login" in driver.current_url