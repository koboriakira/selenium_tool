import requests
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from tjpw_schedule.infrastructure.Item_entity import ItemEntity
from tjpw_schedule.domain.scraper import Scraper, DetailUrl, ActiveTableItems
from tjpw_schedule.custom_logging import get_logger

logger = get_logger(__name__)
SELENIUM_URL = os.environ.get("SELENIUM_URL", "http://localhost:4444")
WAIT_TIME = 5


class SeleniumScraper(Scraper):

    def __init__(self, selenium_domain: str | None = None):
        # Seleniumが起動しているか確認
        selenium_url = (selenium_domain or SELENIUM_URL) + "/wd/hub/status"
        response = requests.get(selenium_url)
        if not response.ok or not response.json()["value"]["ready"]:
            msg = "Selenium is not ready. url: " + selenium_url
            logger.exception(msg)
            raise Exception(msg)

    def get_detail_urls(
        self,
        target_year: int,
        target_month: int,
    ) -> list[DetailUrl]:
        url = self._generate_get_detail_api_url(target_year, target_month)
        logger.info(url)
        driver = _get_driver()
        try:
            driver.get(url)
            elements = driver.find_elements(By.CLASS_NAME, "Itemrow__content")
            return [_extract_detail_url_info(element) for element in elements]
        finally:
            driver.quit()

    def scrape_detail(self, url: str) -> ItemEntity:
        """試合詳細を取得"""
        logger.info(url)
        driver = _get_driver()
        try:
            driver.get(url)
            elements = driver.find_elements(By.CLASS_NAME, "Article_Table__item")
            active_table_items = ActiveTableItems.from_web_elements(url, elements)
            return active_table_items.to_entity_with_url()
        finally:
            driver.quit()

    def _generate_get_detail_api_url(self, target_year: int, target_month: int) -> str:
        """URLを生成"""
        params = {"teamId": "tjpw", "yyyymm": f"{target_year}{target_month:02}"}
        return (
            self.DDTPRO_SCHEDULES
            + "?"
            + "&".join([f"{key}={value}" for key, value in params.items()])
        )


def _convert_to_date(date_str: str) -> datetime:
    """
    "2024Year3Month2Date(Saturday)"のような日付文字列をdatetimeに変換
    """
    return datetime.strptime(date_str, "%YYear%mMonth%dDate(%A)")


def _extract_detail_url_info(element: WebElement) -> DetailUrl:
    href = element.get_attribute("href")
    date_row = element.find_element(By.CLASS_NAME, "Itemrow__date")
    event_datetime = _convert_to_date(date_row.text)
    return DetailUrl(value=href, date=event_datetime)


def _get_driver():
    """Seleniumのドライバーを取得"""
    driver = webdriver.Remote(
        command_executor=SELENIUM_URL, options=webdriver.ChromeOptions()
    )
    driver.implicitly_wait(WAIT_TIME)
    return driver
