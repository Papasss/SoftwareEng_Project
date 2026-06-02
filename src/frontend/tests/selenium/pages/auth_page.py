from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(
    driver,
    frontend_url,
    identifier: str = "citizen@example.com",
    password: str = "Citizen123!",
    timeout: int = 15,
):
    wait = WebDriverWait(driver, timeout)

    driver.get(frontend_url)

    wait.until(
        EC.element_to_be_clickable(
            (By.ID, "login-link")
        )
    ).click()

    wait.until(
        EC.presence_of_element_located(
            (By.ID, "login-form")
        )
    )

    identifier_input = driver.find_element(
        By.ID,
        "login-identifier"
    )

    password_input = driver.find_element(
        By.ID,
        "login-password"
    )

    identifier_input.clear()
    identifier_input.send_keys(identifier)

    password_input.clear()
    password_input.send_keys(password)

    driver.find_element(
        By.ID,
        "login-submit"
    ).click()

    wait.until(
        lambda d:
            "/operator" in d.current_url
            or "/admin" in d.current_url
            or len(d.find_elements(By.ID, "dashboard-page")) > 0
    )