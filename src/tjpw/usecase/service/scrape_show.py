from src.tjpw.domain.schedule_external_api import (
    ScheduleExternalApi,
)
from src.tjpw.domain.scraper import DetailUrl, Scraper


class ScrapeShow:
    def __init__(
        self,
        scraper: Scraper,
        schedule_external_api_list: list[ScheduleExternalApi],
    ) -> None:
        self.scraper = scraper
        self.schedule_external_api_list = schedule_external_api_list

    def execute(self, detail_url: DetailUrl) -> None:
        """詳細をスクレイピングして登録する"""
