from datetime import datetime, timezone, timedelta
from tjpw_schedule.custom_logging import get_logger
from tjpw_schedule.usecase.scrape_tjpw import ScrapeTjpw

JST = timezone(timedelta(hours=+9), "JST")
logger = get_logger(__name__)


def main():
    logger.info("Start main function")
    scrape_tjpw_use_case = ScrapeTjpw()

    start_date = datetime.now(JST)
    end_date = start_date + timedelta(days=7)

    _ = scrape_tjpw_use_case.execute(start_date, end_date)
    logger.info("End main function")


if __name__ == "__main__":
    # python -m tjpw_schedule
    main()
