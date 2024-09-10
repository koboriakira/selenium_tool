from datetime import datetime, timedelta, timezone

from tjpw_schedule.domain.schedule_external_api import (
    ScheduleExternalApi,
)
from tjpw_schedule.domain.scraper import DetailUrl, Scraper


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


if __name__ == "__main__":
    # python -m tjpw_schedule.usecase.service.scrape_show
    from tjpw_schedule.domain.schedule_external_api import ScheduleGoogleCalendarApi
    from tjpw_schedule.infrastructure.selenium_scraper import SeleniumScraper

    suite = ScrapeShow(
        scraper=SeleniumScraper(selenium_domain="http://localhost:4444"),
        schedule_external_api_list=[ScheduleGoogleCalendarApi()],
    )
    JST = timezone(timedelta(hours=+9), "JST")
    suite.execute(
        DetailUrl(
            value="https://www.ddtpro.com/schedules/22723",
            date=datetime(2024, 8, 23, tzinfo=JST),
        )
    )
