from tjpw_schedule.interface.selenium.tjpw_scraper import TjpwScraper
from tjpw_schedule.interface.notion.notion_api import NotionApi
from datetime import datetime


def main():
    scraper = TjpwScraper()
    notion_api = NotionApi()

    tournament_schedules = scraper.scrape(start_date=datetime(2023, 10, 1),
                                          end_date=datetime(2023, 10, 1))
    for tournament_schedule in tournament_schedules:
        notion_api.regist_tournament_schedule(tournament_schedule)


if __name__ == "__main__":
    # python -m tjpw_schedule
    main()
