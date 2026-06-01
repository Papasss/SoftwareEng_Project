import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.auth_page import login


def test_uc14_create_category_as_admin(driver, frontend_url):
    """UC-14: Manage categories - admin can create a new category via admin UI."""
    wait = WebDriverWait(driver, 15)

    login(driver, frontend_url, identifier="admin@example.com", password="Admin123!")

    driver.get(f"{frontend_url}/admin")
    wait.until(EC.presence_of_element_located((By.ID, "admin-categories-title")))

    unique = str(int(time.time() * 1000))
    name = f"Selenium Category {unique}"
    driver.find_element(By.ID, "admin-new-category-name").send_keys(name)
    driver.find_element(By.ID, "admin-new-category-submit").click()

    # Wait for categories table and check the new name appears
    wait.until(EC.presence_of_element_located((By.ID, "admin-categories-table-body")))
    body = driver.find_element(By.ID, "admin-categories-table-body").text
    assert name in body, "New category name not present in admin categories table"
