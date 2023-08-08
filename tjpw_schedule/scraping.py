import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait


def execute():
    selenium_url = os.environ["SELENIUM_URL"]
    print(selenium_url)
    response = requests.get(selenium_url + "/wd/hub/status")
    if not response.json()["value"]["ready"]:
        raise Exception("Selenium is not ready")

    try:
        driver = webdriver.Remote(
            command_executor=selenium_url,
            options=webdriver.ChromeOptions()
        )
        print("get")
        driver.implicitly_wait(5)
        driver.get("https://www.ddtpro.com/schedules?teamId=tjpw")
        print("wait")
        elements = driver.find_elements(By.CLASS_NAME, "Itemrow__content")
        for element in elements:
            print(element.get_attribute("href"))
    finally:
        driver.quit()


if __name__ == "__main__":
    # python -m tjpw_schedule.scraping
    execute()
