from selenium.webdriver.common.by import By

from common.printer import CliPrinter, NullPrinter, Printer
from common.selenium_factory import SeleniumFactory


class ScrapeSchedules:
    def __init__(self, printer: Printer | None = None) -> None:
        self.printer = printer or NullPrinter()

    def execute(self, url: str) -> list[dict[str, str]]:
        """
        スケジュール一覧を取得。 \n
        下記のような dict のリストを返す。 \n
        {\n
          'href': 'https://www.ddtpro.com/schedules/23289',\n
          'dateStr': '2024Year11Month3Date(Sunday)'\n
        }
        """
        if "https://www.ddtpro.com/schedules" not in url:
            msg = "URLが不正です"
            raise ValueError(msg)

        self.printer.print(url)
        driver = SeleniumFactory.get_driver()
        try:
            driver.get(url)
            elements = driver.find_elements(By.CLASS_NAME, "Itemrow__content")
            result = []
            for element in elements:
                href = element.get_attribute("href") or ""
                if "schedules" not in href:
                    title_text = element.find_element(By.CLASS_NAME, "Itemrow__title").text
                    self.printer.print(f"試合以外の予定のため除外 {title_text}")
                    continue

                date_row = element.find_element(By.CLASS_NAME, "Itemrow__date")
                result.append({"href": href, "date": date_row.text})
            return result
        finally:
            driver.quit()


if __name__ == "__main__":
    # python -m src.tjpw.infrastructure.scrape_schedules
    sample_url = "https://www.ddtpro.com/schedules?teamId=tjpw&yyyymm=202411"
    printer = CliPrinter()
    print(ScrapeSchedules(printer=printer).execute(sample_url))
