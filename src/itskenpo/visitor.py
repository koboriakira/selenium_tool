import os
from logging import Logger, getLogger
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located, presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from common.printer import CliPrinter
from common.selenium_factory import SeleniumFactory

WAIT_TIME = 5
SELENIUM_DOMAIN = os.environ.get("SELENIUM_DOMAIN", "http://localhost:4444")

# s=**** の値はもしかしたら都度変わるかもしれない
# その場合は、手動でアクセスしてトークン部分を取得すること
DEFAULT_URL = "https://as.its-kenpo.or.jp/apply/calendar?s=PT13TjJnVFBrbG1KbFZuYzAxVFp5Vkhkd0YyWWZWR2JuOTJiblpTWjFKSGQ5a0hkdzFXWg%3D%3D"

TIME_ROW = "time-row"
DATA_JOIN_TIME = "data-join-time"
DATA_USE_TIME = "data-use-time"


class Visitor:
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

    def access_restaurant(self, restaurant_name: str) -> None:
        """レストランのページにアクセス"""
        self._logger.debug(f"{restaurant_name}のページにアクセス")  # noqa: G004

        # とりあえず予約ページを開く
        self._driver.get(DEFAULT_URL)

        # レストラン名をクリック
        element = self._find_element(By.XPATH, f"//span[text()='{restaurant_name}']")
        self._click(element)

    def click_tab(self, tab_id: str) -> None:
        """タブをクリック"""
        self._logger.debug("タブをクリック %s", tab_id)
        element = self._find_element(By.ID, tab_id)
        self._click(element)

    def get_table_properties(self, table_id: str) -> list[dict[str, str]]:
        self._logger.debug("テーブルを処理 %s ", table_id)

        # テーブルの要素を取得
        tbody_element = self._find_element(By.ID, table_id)

        # td要素を取得
        td_elements = tbody_element.find_elements(By.TAG_NAME, "td")

        result = []
        for td_element in td_elements:
            # classがtime-rowなら無視
            if td_element.get_attribute("class") == TIME_ROW:
                self._logger.debug("classがtime-rowなら無視")
                continue

            # data-join-time属性を取得
            date_ = td_element.get_attribute(DATA_JOIN_TIME) if td_element.get_attribute(DATA_JOIN_TIME) else ""
            time_ = td_element.get_attribute(DATA_USE_TIME) if td_element.get_attribute(DATA_USE_TIME) else ""
            if not date_ or not time_:
                msg = "date_ or time_ is empty"
                raise Exception(msg)

            text = td_element.text
            result.append(
                {
                    "date": date_,
                    "time": time_,
                    "text": text,
                },
            )
        return result

    def click_next_week(self) -> None:
        """次の週へ"""
        self._logger.debug("次の週へ")
        elements = self._find_elements(By.CLASS_NAME, "next-week")

        # いっぱい要素が見つかってしまうので、そのうち表示されているものを見つけてクリックする
        for element in elements:
            if element.is_displayed():
                self._click(element)

    def quit(self) -> None:
        self._driver.quit()

    def _click(self, element: WebElement) -> None:
        """クリック"""
        element.click()
        sleep(self._wait_time)

    def _find_element(self, locator_key: str, value: str) -> WebElement:
        """要素を探す"""
        return WebDriverWait(self._driver, 10).until(
            presence_of_element_located((locator_key, value)),
        )

    def _find_elements(self, locator_key: str, value: str) -> list[WebElement]:
        """要素を探す"""
        return WebDriverWait(self._driver, 10).until(
            presence_of_all_elements_located((locator_key, value)),
        )
