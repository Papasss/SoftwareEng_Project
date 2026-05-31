from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_uc02_login_success(driver, frontend_url):
    """UC-02: Login main success scenario.

    - Navigate to login page
    - Enter seeded citizen credentials and submit
    - Assert redirect to user dashboard
    """
    wait = WebDriverWait(driver, 10)

    driver.get(frontend_url)
    wait.until(EC.element_to_be_clickable((By.ID, "login-link"))).click()

    wait.until(EC.presence_of_element_located((By.ID, "login-form")))
    driver.find_element(By.ID, "login-identifier").clear()
    driver.find_element(By.ID, "login-identifier").send_keys("citizen@example.com")
    driver.find_element(By.ID, "login-password").clear()
    driver.find_element(By.ID, "login-password").send_keys("Citizen123!")
    driver.find_element(By.ID, "login-submit").click()

    # Landing page should show dashboard for a citizen
    wait.until(EC.presence_of_element_located((By.ID, "dashboard-page")))
    assert "User dashboard" in driver.page_source


def test_uc02_login_invalid_credentials(driver, frontend_url):
    """UC-02 extension: invalid credentials should show an error and not authenticate."""
    wait = WebDriverWait(driver, 10)

    driver.get(frontend_url)
    wait.until(EC.element_to_be_clickable((By.ID, "login-link"))).click()
    wait.until(EC.presence_of_element_located((By.ID, "login-form")))

    driver.find_element(By.ID, "login-identifier").clear()
    driver.find_element(By.ID, "login-identifier").send_keys("nonexistent@example.com")
    driver.find_element(By.ID, "login-password").clear()
    driver.find_element(By.ID, "login-password").send_keys("wrongpassword")
    driver.find_element(By.ID, "login-submit").click()

    # Expect an error message to appear
    wait.until(EC.presence_of_element_located((By.ID, "login-error")))
    assert "Invalid" in driver.find_element(By.ID, "login-error").text or "Unable" in driver.find_element(By.ID, "login-error").text
