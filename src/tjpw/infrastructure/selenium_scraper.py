import os
from datetime import datetime

from src.custom_logging import get_logger
from src.tjpw.domain.scraper import DetailUrl, Scraper

from tjpw.domain.schedule import TournamentSchedule
from tjpw.infrastructure.scrape_schedules import ScrapeSchedules
from tjpw.infrastructure.show_scraper import ShowScraper

logger = get_logger(__name__)
SELENIUM_DOMAIN = os.environ.get("SELENIUM_DOMAIN", "http://localhost:4444")
WAIT_TIME = 5


class SeleniumScraper(Scraper):
    def get_detail_urls(
        self,
        target_year: int,
        target_month: int,
    ) -> list[DetailUrl]:
        url = self._generate_get_detail_api_url(target_year, target_month)
        scraped_results = ScrapeSchedules().execute(url)
        details: list[DetailUrl] = []
        for result in scraped_results:
            href = result["href"]
            if "schedules" not in href:
                print(f"試合以外の予定のため除外 {result}")
                continue
            date_str = result["date"]
            date_ = datetime.strptime(date_str, "%YYear%mMonth%dDate(%A)")  # noqa: DTZ007
            details.append(DetailUrl(value=href, date=date_))
        return details

    def scrape_detail(self, url: str) -> TournamentSchedule:
        """試合詳細を取得"""
        scraped_result = ShowScraper().execute(url)
        return TournamentSchedule.from_dict(scraped_result)

    def _generate_get_detail_api_url(self, target_year: int, target_month: int) -> str:
        """URLを生成"""
        params = {"teamId": "tjpw", "yyyymm": f"{target_year}{target_month:02}"}
        return self.DDTPRO_SCHEDULES + "?" + "&".join([f"{key}={value}" for key, value in params.items()])
