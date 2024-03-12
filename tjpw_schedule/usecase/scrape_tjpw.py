from tjpw_schedule.domain.scraper import Scraper, ActiveTableItems
from tjpw_schedule.domain.schedule_external_api import (
    ScheduleExternalApi,
    ScheduleGoogleCalendarApi,
    ScheduleNotionApi,
    ScheduleMockApi,
)
from datetime import datetime
from tjpw_schedule.domain.schedule import TournamentSchedule
from dateutil.relativedelta import relativedelta
from tjpw_schedule.usecase.request.scrape_range import ScrapeRange


class ScrapeTjpw:

    def __init__(
        self,
        scraper: Scraper | None = None,
        schedule_external_api_list: list[ScheduleExternalApi] | None = None,
    ) -> None:
        from tjpw_schedule.infrastructure.selenium_scraper import SeleniumScraper

        self.scraper = scraper or SeleniumScraper()
        self.schedule_external_api_list = schedule_external_api_list or [
            ScheduleGoogleCalendarApi(),
            ScheduleNotionApi(),
            # ScheduleMockApi()
        ]

    def execute(self, range: ScrapeRange) -> None:
        for target_yyyymm in range.to_target_yyyymm_list():
            print(f"target_yyyymm: {target_yyyymm}")
            # その月にふくまれる、試合詳細のURL一覧を取得
            detail_urls = self.scraper.get_detail_urls(
                target_year=int(target_yyyymm[:4]), target_month=int(target_yyyymm[4:])
            )
            # 検索範囲内かつ必要なページに絞る
            detail_urls = [
                detail_url
                for detail_url in detail_urls
                if detail_url.is_in_date_range(range.start_date, range.end_date)
                and detail_url.is_schedule()
            ]
            # それぞれの詳細をスクレイピング
            item_entities = [
                self.scraper.scrape_detail(detail_url.value)
                for detail_url in detail_urls
            ]
            tournament_schedules = [
                item_entity.convert_to_tournament_schedule()
                for item_entity in item_entities
            ]
            # 登録
            for tournament_schedule in tournament_schedules:
                for schedule_external_api in self.schedule_external_api_list:
                    schedule_external_api.save(tournament_schedule)


def _make_date_list(start_date: datetime, end_date: datetime) -> list[datetime]:
    """start_dateからend_dateまでの日付のリストを作成"""
    date_list = []
    while start_date <= end_date:
        date_list.append(start_date)
        start_date += relativedelta(months=1)
    print(f"make_date_list: {date_list}")
    return date_list
