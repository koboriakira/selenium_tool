import os
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from logging import getLogger

from tjpw.domain.schedule import TournamentSchedule

logger = getLogger(__name__)

SELENIUM_DOMAIN = os.environ.get("SELENIUM_DOMAIN", "http://localhost:4444")
WAIT_TIME = 5


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
