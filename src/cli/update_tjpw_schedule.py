from common.printer import CliPrinter
from tjpw.controller.tjpw_scrape_controller import TjpwScrapeController


def main() -> None:
    TjpwScrapeController().scrape(printer=CliPrinter())


if __name__ == "__main__":
    # python -m src.cli.update_tjpw_schedule
    main()
