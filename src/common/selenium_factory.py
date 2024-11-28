import os

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.custom_logging import get_logger

logger = get_logger(__name__)
SELENIUM_DOMAIN = os.environ.get("SELENIUM_DOMAIN", "http://localhost:4444")
WAIT_TIME = 5


class SeleniumFactory:
    def __init__(self, selenium_domain: str | None = None):
        # Seleniumが起動しているか確認
        self._selenium_domain = selenium_domain or SELENIUM_DOMAIN
        selenium_url = self._selenium_domain + "/wd/hub/status"
        response = requests.get(selenium_url)
        if not response.ok or not response.json()["value"]["ready"]:
            msg = "Selenium is not ready. url: " + selenium_url
            logger.exception(msg)
            raise Exception(msg)

    def get_driver(self) -> WebDriver:
        """Seleniumのドライバーを取得"""
        driver = webdriver.Remote(
            command_executor=self._selenium_domain,
            options=webdriver.ChromeOptions(),
        )
        driver.implicitly_wait(WAIT_TIME)
        return driver
