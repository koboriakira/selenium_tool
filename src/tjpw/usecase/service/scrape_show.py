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
        # スクレイピング
        item_entity = self.scraper.scrape_detail(detail_url.value)
        tournament_schedule = item_entity.convert_to_tournament_schedule()

        # 注入したAPIの分、登録処理を行う
        for schedule_external_api in self.schedule_external_api_list:
            schedule_external_api.save(tournament_schedule)
