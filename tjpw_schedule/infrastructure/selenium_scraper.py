from abc import ABCMeta, abstractmethod
import requests
import os
from logging import getLogger
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from tjpw_schedule.domain.schedule import TournamentSchedule
from tjpw_schedule.interface.selenium.Item_entity import ItemEntity
from dataclasses import dataclass
from enum import Enum
from tjpw_schedule.domain.scraper import Scraper, DetailUrl, ActiveTableItems

logger = getLogger(__name__)
SELENIUM_URL = os.environ.get("SELENIUM_URL", "http://localhost:4444")
WAIT_TIME = 5


class SeleniumScraper(Scraper):

    def __init__(self, selenium_domain: str | None = None):
        # Seleniumが起動しているか確認
        selenium_url = (selenium_domain or SELENIUM_URL) + "/wd/hub/status"
        print(selenium_url)
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
        params = {"teamId": "tjpw", "yyyymm": f"{target_year}{target_month:02}"}
        url = (
            self.DDTPRO_SCHEDULES
            + "?"
            + "&".join([f"{key}={value}" for key, value in params.items()])
        )
        logger.info(url)

        driver = _get_driver()
        try:
            result: list[DetailUrl] = []
            driver.get(url)
            elements = driver.find_elements(By.CLASS_NAME, "Itemrow__content")
            for element in elements:
                href = element.get_attribute("href")
                if "https://www.ddtpro.com/schedules" not in href:
                    continue
                date_row = element.find_element(By.CLASS_NAME, "Itemrow__date")
                logger.debug(date_row.text)
                event_datetime = _convert_to_date(date_row.text)
                logger.debug(event_datetime)
                result.append(DetailUrl(value=href, date=event_datetime))
            logger.info(result)
            return result
        finally:
            driver.quit()

    def scrape_detail(self, url: str) -> ActiveTableItems:
        """試合詳細を取得"""
        logger.info(url)
        driver = _get_driver()
        try:
            driver.get(url)
            elements = driver.find_elements(By.CLASS_NAME, "Article_Table__item")
            return ActiveTableItems.from_web_elements(url, elements)
        finally:
            driver.quit()


def _convert_to_date(date_str: str) -> datetime:
    """
    "2024Year3Month2Date(Saturday)"のような日付文字列をdatetimeに変換
    """
    return datetime.strptime(date_str, "%YYear%mMonth%dDate(%A)")


def _get_driver():
    """Seleniumのドライバーを取得"""
    driver = webdriver.Remote(
        command_executor=SELENIUM_URL, options=webdriver.ChromeOptions()
    )
    driver.implicitly_wait(WAIT_TIME)
    return driver
