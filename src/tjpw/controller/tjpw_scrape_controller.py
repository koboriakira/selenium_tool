from datetime import timedelta, timezone

from src.custom_logging import get_logger
from src.tjpw.domain.schedule_external_api import ScheduleGoogleCalendarApi
from src.tjpw.infrastructure.selenium_scraper import SeleniumScraper
from src.tjpw.usecase.request.scrape_range import ScrapeRange
from src.tjpw.usecase.scrape_tjpw import ScrapeTjpw

from common.printer import NullPrinter, Printer
from common.selenium_factory import SeleniumFactory

JST = timezone(timedelta(hours=+9), "JST")
logger = get_logger(__name__)


class TjpwScrapeController:
    def scrape(self, printer: Printer | None = None) -> None:
        printer = printer or NullPrinter()
        if not SeleniumFactory.is_healthy():
            print("Selenium is not healthy")
            return
        scrape_tjpw_usecase = ScrapeTjpw(
            scraper=SeleniumScraper(printer=printer),
            schedule_external_api_list=[ScheduleGoogleCalendarApi()],
            printer=printer,
        )
        scrape_tjpw_usecase.execute(ScrapeRange.create_default_instance())


if __name__ == "__main__":
    # python -m src.tjpw.controller.tjpw_scrape_controller
    controller = TjpwScrapeController()
    controller.scrape()
