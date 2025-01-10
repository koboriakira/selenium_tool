import os
from datetime import datetime

from src.custom_logging import get_logger
from src.tjpw.domain.scraper import DetailUrl, Scraper

from common.printer import CliPrinter, Printer
from tjpw.domain.schedule import TournamentSchedule
from tjpw.infrastructure.schedule_scraper import ScheduleScraper
from tjpw.infrastructure.show_scraper import ShowScraper

logger = get_logger(__name__)
SELENIUM_DOMAIN = os.environ.get("SELENIUM_DOMAIN", "http://localhost:4444")
WAIT_TIME = 5


class SeleniumScraper(Scraper):
    def __init__(self, printer: Printer) -> None:
        self._printer = printer

    def get_detail_urls(
        self,
        target_year: int,
        target_month: int,
    ) -> list[DetailUrl]:
        try:
            url = self._generate_get_detail_api_url(target_year, target_month)
            scraped_results = ScheduleScraper(self._printer).execute(url)
            details: list[DetailUrl] = []
            for result in scraped_results:
                href = result["href"]
                if "schedules" not in href:
                    self._printer.print(f"試合以外の予定のため除外 {result}")
                    continue
                date_str = result["date"]
                date_ = datetime.strptime(date_str, "%YYear%mMonth%dDate(%A)")  # noqa: DTZ007
                details.append(DetailUrl(value=href, date=date_))
            return details
        except Exception as e:
            print(e)
            raise e

    def scrape_detail(self, url: str) -> TournamentSchedule:
        """試合詳細を取得"""
        scraped_result = ShowScraper(self._printer).execute(url)
        return TournamentSchedule.from_dict(scraped_result)

    def _generate_get_detail_api_url(self, target_year: int, target_month: int) -> str:
        """URLを生成"""
        params = {"teamId": "tjpw", "yyyymm": f"{target_year}{target_month:02}"}
        return self.DDTPRO_SCHEDULES + "?" + "&".join([f"{key}={value}" for key, value in params.items()])


if __name__ == "__main__":
    # python -m src.tjpw.infrastructure.selenium_scraer
    printer = CliPrinter()
    suite = SeleniumScraper(printer)
    # print(suite.get_detail_urls(target_year=2025, target_month=3))
    print(suite.scrape_detail(url="https://www.ddtpro.com/schedules/23860"))
