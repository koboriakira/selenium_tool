from datetime import timedelta, timezone

from tjpw_schedule.custom_logging import get_logger
from tjpw_schedule.tjpw.domain.schedule_external_api import ScheduleGoogleCalendarApi
from tjpw_schedule.tjpw.infrastructure.selenium_scraper import SeleniumScraper
from tjpw_schedule.tjpw.usecase.request.scrape_range import ScrapeRange
from tjpw_schedule.tjpw.usecase.scrape_tjpw import ScrapeTjpw

JST = timezone(timedelta(hours=+9), "JST")
logger = get_logger(__name__)


class TjpwScrapeController:
    def scrape(self) -> None:
        logger.debug("Start main function")
        range = ScrapeRange.create_default_instance(is_dev=True)
        scrape_tjpw_usecase = ScrapeTjpw(
            scraper=SeleniumScraper(),
            schedule_external_api_list=[ScheduleGoogleCalendarApi()],
        )
        scrape_tjpw_usecase.execute(range)
        logger.debug("End main function")


if __name__ == "__main__":
    # python -m tjpw_schedule.tjpw.controller.tjpw_scrape_controller
    controller = TjpwScrapeController()
    controller.scrape()
