from datetime import datetime, timezone, timedelta
from tjpw_schedule.custom_logging import get_logger
from tjpw_schedule.usecase.scrape_tjpw import ScrapeTjpw
from tjpw_schedule.usecase.request.scrape_range import ScrapeRange

JST = timezone(timedelta(hours=+9), "JST")
logger = get_logger(__name__)


def main():
    logger.info("Start main function")
    scrape_tjpw_use_case = ScrapeTjpw()

    range = ScrapeRange.create_default_instance()

    scrape_tjpw_use_case.execute(range)
    logger.info("End main function")


if __name__ == "__main__":
    # python -m tjpw_schedule
    main()
