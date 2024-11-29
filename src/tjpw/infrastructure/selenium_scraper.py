import os
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from src.custom_logging import get_logger
from src.tjpw.domain.scraper import ActiveTableItems, DetailUrl, Scraper
from src.tjpw.infrastructure.Item_entity import ItemEntity

logger = get_logger(__name__)
SELENIUM_DOMAIN = os.environ.get("SELENIUM_DOMAIN", "http://localhost:4444")
WAIT_TIME = 5


class SeleniumScraper(Scraper):
    def __init__(self, driver: WebDriver) -> None:
        # Seleniumが起動しているか確認
        self._driver = driver

    def get_detail_urls(
        self,
        target_year: int,
        target_month: int,
    ) -> list[DetailUrl]:
        url = self._generate_get_detail_api_url(target_year, target_month)
        print(url)
        self._driver.get(url)
        elements = self._driver.find_elements(By.CLASS_NAME, "Itemrow__content")
        details = [_extract_detail_url_info(element) for element in elements]
        return [detail for detail in details if detail is not None]

    def scrape_detail(self, url: str) -> ItemEntity:
        """試合詳細を取得"""
        print(url)
        self._driver.get(url)
        elements = self._driver.find_elements(By.CLASS_NAME, "Article_Table__item")
        active_table_items = ActiveTableItems.from_web_elements(url, elements)
        return active_table_items.to_entity_with_url()

    def _generate_get_detail_api_url(self, target_year: int, target_month: int) -> str:
        """URLを生成"""
        params = {"teamId": "tjpw", "yyyymm": f"{target_year}{target_month:02}"}
        return self.DDTPRO_SCHEDULES + "?" + "&".join([f"{key}={value}" for key, value in params.items()])


def _convert_to_date(date_str: str) -> datetime:
    """
    "2024Year3Month2Date(Saturday)"のような日付文字列をdatetimeに変換
    """
    return datetime.strptime(date_str, "%YYear%mMonth%dDate(%A)")  # noqa: DTZ007


def _extract_detail_url_info(element: WebElement) -> DetailUrl | None:
    href = element.get_attribute("href") or ""
    if "schedules" not in href:
        title_text = element.find_element(By.CLASS_NAME, "Itemrow__title").text
        print(f"試合以外の予定のため除外 {title_text}")
        return None

    date_row = element.find_element(By.CLASS_NAME, "Itemrow__date")
    event_datetime = _convert_to_date(date_row.text)
    return DetailUrl(value=href, date=event_datetime)
