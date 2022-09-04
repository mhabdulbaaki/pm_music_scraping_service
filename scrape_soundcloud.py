from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')


def soundcloud_followers(driver, url: str = None):
    xpath = "//*[@id='content']/div/div[4]/div[2]/div/article[1]/table/tbody/tr/td[1]/a/div"
    print('now scraping soundcloud....')
    if url:
        try:
            driver.get(url)
            r_ = WebDriverWait(driver, 3).until(lambda d: d.find_element(By.XPATH, xpath))
            soup = BeautifulSoup(r_.get_attribute("outerHTML"), "html.parser")
            return int(soup.get_text().replace(",", ""))
        except Exception as e:
            print(e)
            return None

    return None


if __name__ == "__main__":
    webdriver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                 options=options)  # headless driver

    soundcloud = "https://soundcloud.com/sarkodie-music"

    result = soundcloud_followers(driver=webdriver, url=soundcloud)
    print(result)
