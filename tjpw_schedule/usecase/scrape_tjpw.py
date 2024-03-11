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

    def execute(self, start_date: datetime, end_date: datetime) -> None:
        print(f"start_date: {start_date.isoformat()}, end_date: {end_date.isoformat()}")
        for target_month in _make_date_list(start_date, end_date):
            _ = self._scrape_month(
                target_year=target_month.year,
                target_month=target_month.month,
                start_date=start_date,
                end_date=end_date,
            )

    def _scrape_month(
        self,
        target_year: int,
        target_month: int,
        start_date: datetime,
        end_date: datetime,
    ) -> list[TournamentSchedule]:
        print(f"target_year: {target_year}, target_month: {target_month}")
        # その月にふくまれる、試合詳細のURL一覧を取得
        detail_urls = self.scraper.get_detail_urls(
            target_year=target_year, target_month=target_month
        )
        # 検索範囲内かつ必要なページに絞る
        detail_urls = [
            detail_url
            for detail_url in detail_urls
            if detail_url.is_in_date_range(start_date, end_date)
            and detail_url.is_schedule()
        ]
        # それぞれの詳細をスクレイピング
        item_entities = [
            self.scraper.scrape_detail(detail_url.value) for detail_url in detail_urls
        ]
        tournament_schedules = [
            item_entity.convert_to_tournament_schedule()
            for item_entity in item_entities
        ]
        # 登録
        for tournament_schedule in tournament_schedules:
            for schedule_external_api in self.schedule_external_api_list:
                schedule_external_api.save(tournament_schedule)
        return tournament_schedules


def _make_date_list(start_date: datetime, end_date: datetime) -> list[datetime]:
    """start_dateからend_dateまでの日付のリストを作成"""
    date_list = []
    while start_date <= end_date:
        date_list.append(start_date)
        start_date += relativedelta(months=1)
    print(f"make_date_list: {date_list}")
    return date_list
