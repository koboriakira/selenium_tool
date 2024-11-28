import os
from datetime import datetime
from enum import Enum
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from common.selenium_factory import SeleniumFactory
from src.custom_logging import get_logger

logger = get_logger(__name__)
SELENIUM_DOMAIN = os.environ.get("SELENIUM_DOMAIN", "http://localhost:4444")
WAIT_TIME = 5

# s=**** の値はもしかしたら都度変わるかもしれない
# その場合は、手動でアクセスしてトークン部分を取得すること
DEFAULT_URL = "https://as.its-kenpo.or.jp/apply/calendar?s=PT13TjJnVFBrbG1KbFZuYzAxVFp5Vkhkd0YyWWZWR2JuOTJiblpTWjFKSGQ5a0hkdzFXWg%3D%3D"


# 予約種類
class RESERVATION_TYPE(Enum):
    DINNER_17_TABLE = {
        "label": "ディナー17時・テーブル席",
        "tab_id": "link-2037",
        "table_id": "tcb-2037",
    }
    DINNER_19_TABLE = {
        "label": "ディナー19時・テーブル席",
        "tab_id": "link-2038",
        "table_id": "tcb-2038",
    }
    DINNER_17_COUNTER = {
        "label": "ディナー17時・カウンター席",
        "tab_id": "link-2039",
        "table_id": "tcb-2039",
    }
    DINNER_19_COUNTER = {
        "label": "ディナー19時・カウンター席",
        "tab_id": "link-2040",
        "table_id": "tcb-2040",
    }
    LUNCH_TABLE = {
        "label": "ランチ・テーブル席",
        "tab_id": "link-2041",
        "table_id": "tcb-2041",
    }
    LUNCH_COUNTER = {
        "label": "ランチ・カウンター席",
        "tab_id": "link-2042",
        "table_id": "tcb-2042",
    }

    def tab_id(self) -> str:
        return self.value["tab_id"]

    def table_id(self) -> str:
        return self.value["table_id"]

    def label(self) -> str:
        return self.value["label"]


# 空き予定
class Vacancy:
    datetime_: datetime
    value: str

    @staticmethod
    def of(date_str: str, time_str: str, value: str) -> "Vacancy":
        vacancy = Vacancy()
        vacancy.datetime_ = datetime.strptime(
            f"{date_str} {time_str}:00+0900", "%Y-%m-%d %H:%M:%S%z"
        )
        vacancy.value = value
        return vacancy


class Itskenpo:
    def __init__(self, selenium_domain: str | None = None, wait_time: int = WAIT_TIME):
        # Seleniumが起動しているか確認
        selenium_domain = selenium_domain or SELENIUM_DOMAIN
        self._driver = SeleniumFactory(selenium_domain).get_driver()
        self._wait_time = wait_time

    def _access(self, url: str) -> None:
        """鮨一新のページにアクセス"""
        self._driver.get(url)
        element = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='鮨一新']"))
        )
        self._click(element)

    def _click(self, element: WebElement) -> None:
        """クリック"""
        element.click()
        sleep(self._wait_time)

    def click_tab(self, tab_id: str) -> None:
        """タブをクリック"""
        element = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.ID, tab_id))
        )
        self._click(element)

    def proc_table(self, tab_id: str) -> list[Vacancy]:
        tbody_element = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.ID, tab_id))
        )
        td_elements = tbody_element.find_elements(By.TAG_NAME, "td")
        vacancies = []
        for td_element in td_elements:
            # classがtime-rowなら無視
            if td_element.get_attribute("class") == "time-row":
                continue

            # × または ☓ なら空き無しとして無視
            text = td_element.text
            if text == "×" or text == "☓":
                continue

            # data-join-time属性を取得
            date_ = (
                td_element.get_attribute("data-join-time")
                if td_element.get_attribute("data-join-time")
                else ""
            )
            time_ = (
                td_element.get_attribute("data-use-time")
                if td_element.get_attribute("data-use-time")
                else ""
            )
            if not date_ or not time_:
                raise Exception("date_ or time_ is empty")
            vacancy = Vacancy.of(date_, time_, text)
            print(vacancy.datetime_, vacancy.value)
            vacancies.append(vacancy)
        return vacancies

    def quit(self) -> None:
        self._driver.quit()

    def next(self) -> None:
        elements = WebDriverWait(self._driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "next-week"))
        )
        for element in elements:
            if element.is_displayed():
                self._click(element)

    def execute(self) -> None:
        try:
            # 鮨一新の空きカレンダーページにアクセス
            self._access(DEFAULT_URL)

            # 12週分の空きを取得
            vacancies = []
            for _ in range(0, 8):
                for reservation in RESERVATION_TYPE:
                    print(reservation.label())
                    self.click_tab(reservation.tab_id())
                    week_vacancies = self.proc_table(reservation.table_id())
                    vacancies.extend(week_vacancies)

            #
            print(vacancies)
        finally:
            self.quit()


if __name__ == "__main__":
    # python -m src.itskenpo.itskenpo
    Itskenpo().execute()
