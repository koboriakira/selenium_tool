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

    def execute(
        self, start_date: datetime, end_date: datetime
    ) -> list[TournamentSchedule]:
        month_date_list = _make_date_list(start_date, end_date)
        month_list_for_debug = [
            month_date.strftime("%Y%m") for month_date in month_date_list
        ]
        print(f"date_list: {month_list_for_debug}")

        result: list[TournamentSchedule] = []
        for target_month in month_date_list:
            tournament_schedules = self.scrape_month(
                target_year=target_month.year,
                target_month=target_month.month,
                start_date=start_date,
                end_date=end_date,
            )
            result.extend(tournament_schedules)
            for tournament_schedule in tournament_schedules:
                for schedule_external_api in self.schedule_external_api_list:
                    schedule_external_api.save(tournament_schedule)

        return result

    def scrape_month(
        self,
        target_year: int,
        target_month: int,
        start_date: datetime,
        end_date: datetime,
    ) -> list[TournamentSchedule]:
        # その月にふくまれる、試合詳細のURL一覧を取得
        detail_urls = self.scraper.get_detail_urls(
            target_year=target_year, target_month=target_month
        )
        # 月のすべてを取得しているので、検索範囲内に絞る
        detail_urls = [
            detail_url
            for detail_url in detail_urls
            if detail_url.is_in_date_range(start_date, end_date)
        ]
        # それぞれの詳細をスクレイピング
        result: list[TournamentSchedule] = []
        for detail_url in detail_urls:
            active_table_items = self.scraper.scrape_detail(detail_url.value)
            print(active_table_items.items)
            # それぞれの詳細をTournamentScheduleに変換
            item_entity = active_table_items.to_entity_with_url()
            result.append(item_entity.convert_to_tournament_schedule())
        return result


def _make_date_list(start_date: datetime, end_date: datetime) -> list[datetime]:
    """start_dateからend_dateまでの日付のリストを作成"""
    date_list = []
    while start_date <= end_date:
        date_list.append(start_date)
        start_date += relativedelta(months=1)
    return date_list
