import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from tjpw_schedule.domain.schedule import Item, ItemType, TournamentName, Date, Venue, SeatType, Note
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

SELENIUM_URL = os.environ.get("SELENIUM_URL", "http://localhost:4444")


class Scraping:
    def __init__(self):
        # Seleniumが起動しているか確認
        response = requests.get(SELENIUM_URL + "/wd/hub/status")
        if not response.json()["value"]["ready"]:
            raise Exception("Selenium is not ready")

    def get_detail_urls(self, target_date: datetime):
        """ 試合詳細のURLを取得 """
        # target_dateをyyyymm形式に変換
        target_date_str = target_date.strftime("%Y%m")
        url = f"https://www.ddtpro.com/schedules?teamId=tjpw&yyyymm={target_date_str}"
        print(url)

        driver = self.__get_driver()
        try:
            driver.implicitly_wait(5)
            driver.get(url)
            elements = driver.find_elements(By.CLASS_NAME, "Itemrow__content")
            for element in elements:
                yield element.get_attribute("href")
        finally:
            driver.quit()

    def get_detail(self, url: str):
        """ 試合詳細を取得 """
        driver = self.__get_driver()
        try:
            driver.implicitly_wait(2)
            driver.get(url)
            elements = driver.find_elements(
                By.CLASS_NAME, "Article_Table__item")
            tournament_name = None
            date = None
            venue = None
            seat_type = None
            note = None
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
            return Item(tournament_name, date, venue, seat_type, note if note else None)
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

    # 2023年8月1日から、1ヶ月単位で2024年1月1日までの日付のリストをつくる
    date_list = []
    start_date = datetime(2023, 10, 1)
    end_date = datetime(2024, 1, 1)
    while start_date <= end_date:
        date_list.append(start_date)
        start_date += relativedelta(months=1)

    for target_date in date_list:
        detail_urls = list(scraping.get_detail_urls(target_date=target_date))
        # detail_urlsは試合のほかに選手の誕生日の場合もある
        # TODO: 誕生日はあとで対応するとして、まず試合のみに絞る。URLに`schedule`が含まれているもののみを対象とする
        detail_urls = [url for url in detail_urls if "schedule" in url]
        for detail_url in detail_urls:
            item = scraping.get_detail(detail_url)
            print(item.overview())
            print("\n====================\n")
