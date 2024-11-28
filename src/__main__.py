from tjpw.controller.tjpw_scrape_controller import TjpwScrapeController

from src.custom_logging import get_logger

logger = get_logger(__name__)


if __name__ == "__main__":
    TjpwScrapeController().scrape()
