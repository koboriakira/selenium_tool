import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait

SELENIUM_URL = os.environ.get("SELENIUM_URL", "http://localhost:4444")


class Scraping:
    def __init__(self):
        response = requests.get(SELENIUM_URL + "/wd/hub/status")
        if not response.json()["value"]["ready"]:
            raise Exception("Selenium is not ready")

    @staticmethod
    def get_driver():
        return webdriver.Remote(
            command_executor=SELENIUM_URL,
            options=webdriver.ChromeOptions()
        )

    def get_detail_urls(self):
        driver = self.get_driver()
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
        driver = self.get_driver()
        try:
            print("get")
            driver.implicitly_wait(2)
            driver.get(url)
            print("wait")
            elements = driver.find_elements(
                By.CLASS_NAME, "Article_Table__item")
            for element in elements:
                print(element.text)
        finally:
            driver.quit()


if __name__ == "__main__":
    # python -m tjpw_schedule.scraping
    scraping = Scraping()
    detail_urls = list(scraping.get_detail_urls())
    print(detail_urls)
    for detail_url in detail_urls:
        scraping.get_detail(detail_url)
