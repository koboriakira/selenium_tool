from common.printer import CliPrinter
from common.selenium_factory import NotReadyError, SeleniumFactory
from tjpw.controller.tjpw_scrape_controller import TjpwScrapeController


def main() -> None:
    try:
        SeleniumFactory.validate()
    except NotReadyError:
        print("Seleniumのコンテナが起動していません")
        return
    TjpwScrapeController().scrape(printer=CliPrinter())


if __name__ == "__main__":
    # python -m src.cli.update_tjpw_schedule
    main()
