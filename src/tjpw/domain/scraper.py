import os
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from logging import getLogger

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from src.tjpw.infrastructure.Item_entity import ItemEntity

from tjpw.domain.schedule import TournamentSchedule

logger = getLogger(__name__)

SELENIUM_DOMAIN = os.environ.get("SELENIUM_DOMAIN", "http://localhost:4444")
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

    def key(self) -> str:  # noqa: C901
        match self:
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
    def from_web_element(element: WebElement) -> "ActiveTableItem":
        element_title = element.find_element(By.CLASS_NAME, "Article_Table__title")
        item_type = ItemType(element_title.text)
        element_body = element.find_element(By.CLASS_NAME, "Article_Table__body")
        return ActiveTableItem(item_type=item_type, value=element_body.text)


@dataclass(frozen=True)
class ActiveTableItems:
    url: str
    items: list[ActiveTableItem]

    @staticmethod
    def from_scraped_result(result: list[dict[str, str]]) -> "ActiveTableItems":
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


class Scraper(metaclass=ABCMeta):
    DDTPRO_SCHEDULES = "https://www.ddtpro.com/schedules"

    @abstractmethod
    def get_detail_urls(
        self,
        target_year: int,
        target_month: int,
    ) -> list[DetailUrl]:
        """試合詳細のURLを取得"""

    @abstractmethod
    def scrape_detail(self, url: str) -> TournamentSchedule:
        """試合詳細を取得"""
