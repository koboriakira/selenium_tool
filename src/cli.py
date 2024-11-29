from common.printer import CliPrinter
from src.custom_logging import get_logger
from tjpw.controller.tjpw_scrape_controller import TjpwScrapeController

logger = get_logger(__name__)


def tjpw_update_schedule() -> None:
    TjpwScrapeController().scrape(printer=CliPrinter())


if __name__ == "__main__":
    # python -m src.cli
    tjpw_update_schedule()
