import os

import requests
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from src.custom_logging import get_logger

logger = get_logger(__name__)
SELENIUM_DOMAIN = os.environ.get("SELENIUM_DOMAIN", "http://localhost:4444")
WAIT_TIME = 5

driver = None


class SeleniumFactory:
    @staticmethod
    def is_healthy(selenium_domain: str | None = None) -> bool:
        # Seleniumが起動しているか確認
        selenium_domain = selenium_domain or SELENIUM_DOMAIN
        selenium_url = selenium_domain + "/wd/hub/status"
        response = requests.get(selenium_url, timeout=10)
        if not response.ok or not response.json()["value"]["ready"]:
            msg = "Selenium is not ready. url: " + selenium_url
            logger.exception(msg)
            return False
        return True

    @staticmethod
    def get_driver(selenium_domain: str | None = None) -> WebDriver:
        """Seleniumのドライバーを取得"""
        selenium_domain = selenium_domain or SELENIUM_DOMAIN
        driver = webdriver.Remote(
            command_executor=selenium_domain,
            options=webdriver.ChromeOptions(),
        )
        driver.implicitly_wait(WAIT_TIME)
        return driver
