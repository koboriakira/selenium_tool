import logging
import os
from logging import Logger, getLogger
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from common.printer import CliPrinter
from common.selenium_factory import SeleniumFactory
from itskenpo.reservation_type import ReservationType
from itskenpo.vacancy import Vacancy
from src.custom_logging import get_logger

logger = get_logger(__name__)
SELENIUM_DOMAIN = os.environ.get("SELENIUM_DOMAIN", "http://localhost:4444")
WAIT_TIME = 5

# s=**** の値はもしかしたら都度変わるかもしれない
# その場合は、手動でアクセスしてトークン部分を取得すること
DEFAULT_URL = "https://as.its-kenpo.or.jp/apply/calendar?s=PT13TjJnVFBrbG1KbFZuYzAxVFp5Vkhkd0YyWWZWR2JuOTJiblpTWjFKSGQ5a0hkdzFXWg%3D%3D"

MAX_COUNTABLE_WEEKS = 13


class Itskenpo:
    def __init__(
        self,
        selenium_domain: str | None = None,
        wait_time: int = WAIT_TIME,
        logger: Logger | None = None,
    ) -> None:
        # Seleniumが起動しているか確認
        selenium_domain = selenium_domain or SELENIUM_DOMAIN
        self._driver = SeleniumFactory.get_driver(selenium_domain)
        self._wait_time = wait_time
        self._printer = CliPrinter()
        self._logger = logger or getLogger(__name__)

    def _access(self, url: str) -> None:
        """鮨一新のページにアクセス"""
        self._logger.debug("鮨一新のページにアクセス")
        self._driver.get(url)
        element = WebDriverWait(self._driver, 10).until(
            presence_of_element_located((By.XPATH, "//span[text()='鮨一新']")),
        )
        self._click(element)

    def _click(self, element: WebElement) -> None:
        """クリック"""
        element.click()
        sleep(self._wait_time)

    def click_tab(self, tab_id: str) -> None:
        """タブをクリック"""
        self._logger.debug("タブをクリック %s", tab_id)
        element = WebDriverWait(self._driver, 10).until(
            presence_of_element_located((By.ID, tab_id)),
        )
        self._click(element)

    def proc_table(self, reservation_type: ReservationType) -> list[Vacancy]:
        self._logger.debug("テーブルを処理 %s %s", reservation_type.label(), reservation_type.table_id())
        table_id = reservation_type.table_id()
        tbody_element = WebDriverWait(self._driver, 10).until(
            presence_of_element_located((By.ID, table_id)),
        )
        td_elements = tbody_element.find_elements(By.TAG_NAME, "td")
        vacancies = []
        for td_element in td_elements:
            # classがtime-rowなら無視
            if td_element.get_attribute("class") == "time-row":
                self._logger.debug("classがtime-rowなら無視")
                continue

            # data-join-time属性を取得
            date_ = td_element.get_attribute("data-join-time") if td_element.get_attribute("data-join-time") else ""
            time_ = td_element.get_attribute("data-use-time") if td_element.get_attribute("data-use-time") else ""
            if not date_ or not time_:
                msg = "date_ or time_ is empty"
                raise Exception(msg)

            # 空き無しは無視
            text = td_element.text
            if text in ("×", "☓"):  # noqa: RUF001
                self._logger.debug("%s %s %s %s", date_, time_, reservation_type.label(), text)
                continue

            # 空きあり
            self._logger.info("%s %s %s %s", date_, time_, reservation_type.label(), text)
            vacancy = Vacancy.of(date_, time_, text)
            self._printer.print(vacancy.datetime_, vacancy.value)
            vacancies.append(vacancy)
        return vacancies

    def quit(self) -> None:
        self._driver.quit()

    def next(self) -> None:
        self._logger.debug("次の週へ")
        elements = WebDriverWait(self._driver, 10).until(
            presence_of_all_elements_located((By.CLASS_NAME, "next-week")),
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
            for i in range(MAX_COUNTABLE_WEEKS + 1):
                self._printer.print(f"{i + 1}週目")
                for reservation in ReservationType:
                    self.click_tab(reservation.tab_id())
                    week_vacancies = self.proc_table(reservation)
                    vacancies.extend(week_vacancies)
                self.next()

            self._printer.print(vacancies)
        finally:
            self.quit()


if __name__ == "__main__":
    # python -m src.itskenpo.itskenpo
    logger = getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    Itskenpo(logger=logger).execute()
