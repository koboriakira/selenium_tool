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

logger = getLogger(__name__)

SELENIUM_URL = os.environ.get("SELENIUM_URL", "http://localhost:4444")
WAIT_TIME = 5


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
    url: str
    items: list[ActiveTableItem]

    @staticmethod
    def from_web_elements(url: str, elements: list[WebElement]):
        return ActiveTableItems(
            url=url,
            items=[ActiveTableItem.from_web_element(element) for element in elements],
        )

    def to_entity_with_url(self) -> ItemEntity:
        """ItemEntityに変換"""
        params = {"url": self.url}
        for item in self.items:
            params[item.item_type.key()] = item.value
        return ItemEntity.from_dict(params)


@dataclass(frozen=True)
class DetailUrl:
    value: str
    date: datetime

    def is_in_date_range(self, start_date: datetime, end_date: datetime) -> bool:
        """start_dateからend_dateの範囲内にあるか"""
        return start_date.timestamp() <= self.date.timestamp() <= end_date.timestamp()


class Scraper(metaclass=ABCMeta):
    DDTPRO_SCHEDULES = "https://www.ddtpro.com/schedules"

    @abstractmethod
    def get_detail_urls(
        self,
        target_year: int,
        target_month: int,
    ) -> list[DetailUrl]:
        """試合詳細のURLを取得"""
        pass

    @abstractmethod
    def scrape_detail(self, url: str) -> ActiveTableItems:
        """試合詳細を取得"""