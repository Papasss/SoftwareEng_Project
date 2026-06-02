import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.auth_page import login


def test_uc15_manage_citizen_profile(driver, frontend_url):
    """UC-15: Manage citizen profile - update email notification preference and save."""
    wait = WebDriverWait(driver, 15)

    login(driver, frontend_url, identifier="citizen@example.com", password="Citizen123!")

    # Dashboard/profile area should be visible
    wait.until(EC.presence_of_element_located((By.ID, "profile-form")))

    # Toggle email notifications checkbox and save
    checkbox = driver.find_element(By.ID, "profile-email-notifications")
    checkbox.click()
    driver.find_element(By.ID, "profile-save").click()

    # Wait for success message
    wait.until(EC.presence_of_element_located((By.ID, "profile-success")))
    assert "Profile updated" in driver.find_element(By.ID, "profile-success").text or "Profile updated." in driver.find_element(By.ID, "profile-success").text
