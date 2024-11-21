import os

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tjpw_schedule.custom_logging import get_logger

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


if __name__ == "__main__":
    # python -m tjpw_schedule.infrastructure.selenium_scraper
    scraper = SeleniumScraper("http://localhost:4444")
    url = "https://as.its-kenpo.or.jp/apply/calendar?s=PT13TjJnVFBrbG1KbFZuYzAxVFp5Vkhkd0YyWWZWR2JuOTJiblpTWjFKSGQ5a0hkdzFXWg%3D%3D&join_date=2024-12-01&apply_service_id=2037"
    logger.debug(url)
    driver = _get_driver(scraper._selenium_domain)
    try:
        driver.get(url)
        # tab_element = driver.find_element(By.ID, "tcb-2037")
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='鮨一新']"))
        )
        # 鮨一新に行く
        element.click()
        # print("クリック成功")
        page_title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "page-title"))
        )
        print(page_title_element.text)
        tbody_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tcb-2037"))
        )
        td_elements = tbody_element.find_elements(By.TAG_NAME, "td")
        for td_element in td_elements:
            print(td_element.text)
        # 次のタブに移動
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "link-2038"))
        )
        element.click()
        page_title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "page-title"))
        )
        print(page_title_element.text)
        tbody_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tcb-2038"))
        )
        td_elements = tbody_element.find_elements(By.TAG_NAME, "td")
        for td_element in td_elements:
            print(td_element.text)
    finally:
        driver.quit()
