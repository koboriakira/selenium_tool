from tjpw_schedule.interface.selenium.tjpw_scraper import TjpwScraper
from tjpw_schedule.interface.notion.notion_api import NotionApi
from tjpw_schedule.interface.gas.gas_api import GasApi
from datetime import datetime, timezone, timedelta
from tjpw_schedule.custom_logging import get_logger

JST = timezone(timedelta(hours=+9), "JST")
logger = get_logger(__name__)


def main():
    logger.info("Start main function")
    scraper = TjpwScraper()
    notion_api = NotionApi()
    gas_api = GasApi()

    start_date = datetime.now(JST)
    end_date = datetime.now(JST) + timedelta(days=7)

    tournament_schedules = scraper.scrape(start_date, end_date)
    for tournament_schedule in tournament_schedules:
        notion_api.regist_tournament_schedule(tournament_schedule)
        gas_api.regist_tournament_schedule(tournament_schedule)
    logger.info("End main function")


if __name__ == "__main__":
    # python -m tjpw_schedule
    main()
