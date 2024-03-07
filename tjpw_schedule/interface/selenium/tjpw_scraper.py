import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dataclasses import dataclass
from enum import Enum
from tjpw_schedule.interface.selenium.Item_entity import ItemEntity
from tjpw_schedule.domain.schedule import TournamentSchedule
from tjpw_schedule.custom_logging import get_logger

SELENIUM_URL = os.environ.get("SELENIUM_URL", "http://localhost:4444")
DDTPRO_SCHEDULES = "https://www.ddtpro.com/schedules"
WAIT_TIME = 5

logger = get_logger(__name__)


class ItemType(Enum):
    """情報の種類"""

    # 大会名
    TOURNAMENT_NAME = "大会名"
    # 日時
    DATE = "日時"
    # 会場
    VENUE = "会場"
    # 席種
    SEAT_TYPE = "席種"
    # 備考
    NOTE = "備考"

    def key(self):
        match (self):
            case ItemType.TOURNAMENT_NAME:
                return "tournament_name"
            case ItemType.DATE:
                return "date"
            case ItemType.VENUE:
                return "venue"
            case ItemType.SEAT_TYPE:
                return "seat_type"
            case ItemType.NOTE:
                return "note"


@dataclass(frozen=True)
class ActiveTableItem:
    item_type: ItemType
    value: str

    @staticmethod
    def from_web_element(element: WebElement):
        element_title = element.find_element(By.CLASS_NAME, "Article_Table__title")
        item_type = ItemType(element_title.text)
        element_body = element.find_element(By.CLASS_NAME, "Article_Table__body")
        return ActiveTableItem(item_type=item_type, value=element_body.text)


@dataclass(frozen=True)
class ActiveTableItems:
    items: list[ActiveTableItem]

    @staticmethod
    def from_web_elements(elements: list[WebElement]):
        return ActiveTableItems(
            [ActiveTableItem.from_web_element(element) for element in elements]
        )

    def to_entity_with_url(self, url: str) -> ItemEntity:
        """ItemEntityに変換"""
        params = {"url": url}
        for item in self.items:
            params[item.item_type.key()] = item.value
        return ItemEntity.from_dict(params)


class TjpwScraper:
    def __init__(self):
        # Seleniumが起動しているか確認
        response = requests.get(SELENIUM_URL + "/wd/hub/status")
        if not response.ok or not response.json()["value"]["ready"]:
            msg = "Selenium is not ready. url: " + SELENIUM_URL + "/wd/hub/status"
            logger.exception(msg)
            raise Exception(msg)

    def scrape(
        self, start_date: datetime, end_date: datetime
    ) -> list[TournamentSchedule]:
        month_date_list = _make_date_list(start_date, end_date)
        logger.debug(f"date_list: {month_date_list}")

        result: list[TournamentSchedule] = []
        for target_month in month_date_list:
            monthly_result = self._scrape_month(target_month, start_date, end_date)
            result.extend(monthly_result)

        return result

    def _scrape_month(
        self, target_month: datetime, start_date: datetime, end_date: datetime
    ) -> list[TournamentSchedule]:
        # その月にふくまれる、試合詳細のURL一覧を取得
        detail_urls = self.get_detail_urls(
            target_month=target_month, start_date=start_date, end_date=end_date
        )

        # detail_urlsは試合のほかに選手の誕生日の場合もある
        # TODO: 誕生日はあとで対応するとして、まず試合のみに絞る。URLに`schedule`が含まれているもののみを対象とする
        detail_urls = [url for url in detail_urls if "schedule" in url]

        result = []
        for detail_url in detail_urls:
            tournament_schedule = self.scrape_detail(detail_url)
            logger.info(tournament_schedule)
            result.append(tournament_schedule)
        return result

    def get_detail_urls(
        self, target_month: datetime, start_date: datetime, end_date: datetime
    ) -> list[str]:
        """試合詳細のURLを取得"""
        params = {"teamId": "tjpw", "yyyymm": target_month.strftime("%Y%m")}
        url = (
            DDTPRO_SCHEDULES
            + "?"
            + "&".join([f"{key}={value}" for key, value in params.items()])
        )
        logger.info(url)

        driver = _get_driver()
        try:
            result = []
            driver.implicitly_wait(WAIT_TIME)
            driver.get(url)
            elements = driver.find_elements(By.CLASS_NAME, "Itemrow__content")
            for element in elements:
                date_row = element.find_element(By.CLASS_NAME, "Itemrow__date")
                logger.debug(date_row.text)
                event_datetime = convert_to_date(date_row.text)
                logger.debug(event_datetime)
                # event_datetimeがstart_dateからend_dateの範囲内であれば、URLを取得
                if (
                    start_date.timestamp()
                    <= event_datetime.timestamp()
                    <= end_date.timestamp()
                ):
                    result.append(element.get_attribute("href"))
            logger.info(result)
            return result
        finally:
            driver.quit()

    def scrape_detail(self, url: str) -> TournamentSchedule:
        """試合詳細を取得"""
        logger.info(url)
        driver = _get_driver()
        try:
            driver.implicitly_wait(WAIT_TIME)
            driver.get(url)
            elements = driver.find_elements(By.CLASS_NAME, "Article_Table__item")
            active_table_items = ActiveTableItems.from_web_elements(elements)
            item_entity = active_table_items.to_entity_with_url(url)
            return item_entity.convert_to_tournament_schedule()
        finally:
            driver.quit()


def convert_to_date(date_str: str) -> datetime:
    """
    "2024Year3Month2Date(Saturday)"のような日付文字列をdatetimeに変換
    """
    return datetime.strptime(date_str, "%YYear%mMonth%dDate(%A)")


def _make_date_list(start_date: datetime, end_date: datetime) -> list[datetime]:
    """start_dateからend_dateまでの日付のリストを作成"""
    date_list = []
    while start_date <= end_date:
        date_list.append(start_date)
        start_date += relativedelta(months=1)
    return date_list


def _get_driver():
    """Seleniumのドライバーを取得"""
    return webdriver.Remote(
        command_executor=SELENIUM_URL, options=webdriver.ChromeOptions()
    )


if __name__ == "__main__":
    # python -m tjpw_schedule.interface.selenium.tjpw_scraper
    scraping = TjpwScraper()

    # start_date = datetime(2023, 10, 1)
    # end_date = datetime(2023, 10, 1)
    # print(scraping.scrape(start_date, end_date))

    print(scraping.get_detail_urls(datetime(2024, 3, 8)))
    # print(scraping.scrape_detail(url="https://www.ddtpro.com/schedules/20448"))
