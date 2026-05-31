import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def frontend_url():
    return os.environ.get("FRONTEND_URL", "http://localhost:5173")


@pytest.fixture
def driver():
    """Create a Chrome WebDriver for Selenium tests.

    Requires chromedriver available in PATH. Use env `HEADLESS=0` to disable headless mode.
    """
    options = Options()
    if os.environ.get("HEADLESS", "1") != "0":
        # use the new headless mode if supported
        try:
            options.add_argument("--headless=new")
        except Exception:
            options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    # enable browser console logging to aid debugging in tests
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1200, 900)
    yield driver
    try:
        driver.quit()
    except Exception:
        pass
