from tjpw_schedule.interface.selenium.tjpw_scraper import TjpwScraper
from tjpw_schedule.interface.notion.notion_api import NotionApi
from tjpw_schedule.interface.gas.gas_api import GasApi
from datetime import datetime


def main():
    scraper = TjpwScraper()
    notion_api = NotionApi()
    gas_api = GasApi()

    tournament_schedules = scraper.scrape(start_date=datetime(2023, 11, 1),
                                          end_date=datetime(2023, 11, 1))
    for tournament_schedule in tournament_schedules:
        notion_api.regist_tournament_schedule(tournament_schedule)
        gas_api.regist_tournament_schedule(tournament_schedule)


if __name__ == "__main__":
    # python -m tjpw_schedule
    main()
