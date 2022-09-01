from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
import time

# selenium webdriver setup
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')


def get_artist_media_handles(spotify_url: str):
    """
    takes a spotify artist url
    returns a dictionary of artist social media handles
    returns None if error occurs
    """
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                              options=options)  # headless driver
    driver.get(spotify_url)

    media_handles = {}

    # xpath to 'see more' text button
    x_path = ("//*[@id='main']/div/div[2]/div[3]/div[1]/div[2]/div[2]/"
              "div/div/div[2]/main/section/div/div[2]/div[3]/div[2]/div/div/button/div")

    body_html = driver.find_element(By.TAG_NAME, "html")

    try:
        # click to view more about artist
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 5).
                              until(ec.element_to_be_clickable((By.XPATH, x_path))))

        html = body_html.get_attribute('outerHTML')
        time.sleep(2)
        soup = BeautifulSoup(html, 'html.parser')  # parse html
        body = soup.find("body")  # get html body
        listeners_tag = body.find("div", string="Monthly Listeners")  # get div containing the string Monthly Listeners
        media_handles["monthly_listeners"] = int(listeners_tag.previousSibling.get_text().replace(",", ""))

        # get social media links
        social_media_platforms = ["Twitter", "Facebook", "Instagram"]
        for platform in social_media_platforms:
            sm_tag = body.find("span", string=platform)
            if sm_tag:
                media_handles[platform.lower()] = sm_tag.parent.attrs["href"]
            else:
                media_handles[platform.lower()] = None
                continue
        driver.quit()
        return media_handles

    except Exception as e:
        print(f"an error occurred: \n{e}")
        driver.quit()
        return media_handles


if __name__ == "__main__":
    result = get_artist_media_handles("https://open.spotify.com/artist/6DaTJdntb3yC7zhY2qVzCw")
    print(result)
