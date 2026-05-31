import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_uc01_register_main_success(driver, frontend_url):
    """UC-01: Register account - main success scenario.

    Steps:
    1. Navigate to home and open registration page.
    2. Fill required fields and submit the form.
    3. Wait for the verification link to be exposed and open it.
    4. Assert that the verification endpoint confirms the email.
    """
    wait = WebDriverWait(driver, 15)

    # 1) Go to frontend root and open register page
    driver.get(frontend_url)
    wait.until(EC.element_to_be_clickable((By.ID, "register-link"))).click()

    # 2) Wait for form and fill fields with unique values
    wait.until(EC.presence_of_element_located((By.ID, "register-form")))
    unique = str(int(time.time() * 1000))
    username = f"selenium_{unique}"
    email = f"{username}@example.com"

    driver.find_element(By.ID, "register-username").send_keys(username)
    driver.find_element(By.ID, "register-first-name").send_keys("Selenium")
    driver.find_element(By.ID, "register-last-name").send_keys("Tester")
    driver.find_element(By.ID, "register-email").send_keys(email)
    driver.find_element(By.ID, "register-password").send_keys("Test1234!")

    driver.find_element(By.ID, "register-submit").click()

    # 3) Wait for verification link to appear (exposed in demo/local env)
    wait.until(EC.presence_of_element_located((By.ID, "verification-link")))
    verification_link = driver.find_element(By.ID, "verification-link")

    # open the verification link (may open in same tab or new tab)
    verification_link.click()

    # switch to the newest window (verification endpoint may open in new tab)
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])

    # 4) Assert verification succeeded
    wait.until(lambda d: "Email verified" in d.page_source or '"message": "Email verified."' in d.page_source)
    assert ("Email verified" in driver.page_source) or ('"message": "Email verified."' in driver.page_source)

    # 5) Confirm the account can be used to login (completes UC-01 success guarantees)
    # navigate back to home and open login page
    driver.get(frontend_url)
    wait.until(EC.element_to_be_clickable((By.ID, "login-link"))).click()
    wait.until(EC.presence_of_element_located((By.ID, "login-form")))

    # use the created credentials to log in
    driver.find_element(By.ID, "login-identifier").clear()
    driver.find_element(By.ID, "login-identifier").send_keys(email)
    driver.find_element(By.ID, "login-password").clear()
    driver.find_element(By.ID, "login-password").send_keys("Test1234!")
    driver.find_element(By.ID, "login-submit").click()

    # landing page should show dashboard for a citizen
    wait.until(EC.presence_of_element_located((By.ID, "dashboard-page")))
    assert "User dashboard" in driver.page_source
