import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from tjpw_schedule.domain.schedule import Item, ItemType, TournamentName, Date, Venue, SeatType, Note

SELENIUM_URL = os.environ.get("SELENIUM_URL", "http://localhost:4444")


class Scraping:
    def __init__(self):
        # Seleniumが起動しているか確認
        response = requests.get(SELENIUM_URL + "/wd/hub/status")
        if not response.json()["value"]["ready"]:
            raise Exception("Selenium is not ready")

    def get_detail_urls(self):
        """ 試合詳細のURLを取得 """
        driver = self.__get_driver()
        try:
            print("get")
            driver.implicitly_wait(5)
            driver.get("https://www.ddtpro.com/schedules?teamId=tjpw")
            print("wait")
            elements = driver.find_elements(By.CLASS_NAME, "Itemrow__content")
            for element in elements:
                yield element.get_attribute("href")
        finally:
            driver.quit()

    def get_detail(self, url: str):
        """ 試合詳細を取得 """
        driver = self.__get_driver()
        try:
            print("get")
            driver.implicitly_wait(2)
            driver.get(url)
            print("wait")
            elements = driver.find_elements(
                By.CLASS_NAME, "Article_Table__item")
            print(len(elements))
            for element in elements:
                element_title = element.find_element(
                    By.CLASS_NAME, "Article_Table__title")
                element_body = element.find_element(
                    By.CLASS_NAME, "Article_Table__body")
                item_type = ItemType(element_title.text)
                match (item_type):
                    case ItemType.TOURNAMENT_NAME:
                        tournament_name = TournamentName(element_body.text)
                    case ItemType.DATE:
                        date = Date(element_body.text)
                    case ItemType.VENUE:
                        venue = Venue(element_body.text)
                    case ItemType.SEAT_TYPE:
                        seat_type = SeatType(element_body.text)
                    case ItemType.NOTE:
                        note = Note(element_body.text)
            return Item(tournament_name, date, venue, seat_type, note)
        finally:
            driver.quit()

    @staticmethod
    def __get_driver():
        """ Seleniumのドライバーを取得 """
        return webdriver.Remote(
            command_executor=SELENIUM_URL,
            options=webdriver.ChromeOptions()
        )


if __name__ == "__main__":
    # python -m tjpw_schedule.scraping
    scraping = Scraping()
    # detail_urls = list(scraping.get_detail_urls())
    # print(detail_urls)
    # for detail_url in detail_urls:
    #     scraping.get_detail(detail_url)
    result = scraping.get_detail("https://www.ddtpro.com/schedules/20440")
    print(result)
