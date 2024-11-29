import json

from selenium.webdriver.common.by import By

from common.printer import NullPrinter, Printer
from common.selenium_factory import SeleniumFactory


class ShowScraper:
    def __init__(self, printer: Printer | None = None) -> None:
        self.printer = printer or NullPrinter()

    def execute(self, url: str) -> list[dict[str, str]]:
        """
        試合詳細を取得
        """
        """試合詳細を取得"""
        driver = SeleniumFactory.get_driver()
        try:
            driver.get(url)
            elements = driver.find_elements(By.CLASS_NAME, "Article_Table__item")

            result = [
                {"key": "url", "value": url},
            ]
            for element in elements:
                element_title = element.find_element(By.CLASS_NAME, "Article_Table__title")
                item_type = element_title.text
                element_body = element.find_element(By.CLASS_NAME, "Article_Table__body").text
                result.append({"key": item_type, "value": element_body})
            return result
        finally:
            driver.quit()


if __name__ == "__main__":
    # python -m src.tjpw.infrastructure.show_scraper
    sample_url = "https://www.ddtpro.com/schedules/23289"
    result = ShowScraper().execute(sample_url)
    print(json.dumps(result, ensure_ascii=False, indent=2))
