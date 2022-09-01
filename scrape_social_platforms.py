from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pprint

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')


def facebook_followers(driver, url: str = None):
    """takes a WebDriver and returns the facebook followers count for a Fb page"""

    print("now scraping facebook...")
    if url:
        driver.get(url)
        followers_href = url.split("?")[0] + "followers/"
        followers_href = followers_href.replace("web", "www")

        html_tag = driver.find_element(By.TAG_NAME, "html")
        html = html_tag.get_attribute("outerHTML")  # returns entire html page for the fb url

        soup = BeautifulSoup(html, "html.parser")  # parse html
        a_tag = soup.find(attrs={"href": f"{followers_href}"})  # finds <a> tag with followers information

        followers = a_tag.get_text()  # extracts the followers string
        return followers

    return None


def instagram_followers(driver, url: str = None):
    """takes a WebDriver return number of instagram followers. Else return None if error occurs"""

    print('now scraping instagram....')
    if url:
        try:
            driver.get(url)

            ig_html = driver.find_element(By.TAG_NAME, "html")

            WebDriverWait(driver, 3).until(lambda d: d.find_element(By.CSS_SELECTOR, "button > div > span"))

            ig_page = ig_html.get_attribute("outerHTML")

            ig_soup = BeautifulSoup(ig_page, "html.parser")

            r = ig_soup.select("button > div > span")[1]

            return int(r.attrs["title"].replace(",", ""))
        except Exception as e:
            print(e)
            return None
    print("no url provided")
    return None


def tiktok_followers(driver, url: str = None):
    xpath = "//*[@id='app']/div[2]/div[2]/div/div[1]/h2[1]/div[2]"
    print('now scraping tiktok....')
    if url:
        try:
            driver.get(url)
            r_ = WebDriverWait(driver, 3).until(lambda d: d.find_element(By.XPATH, xpath))
            soup = BeautifulSoup(r_.get_attribute("outerHTML"), "html.parser")
            return soup.find(attrs={"title": "Followers"}).text
        except Exception as e:
            print(e)
            return None

    return None


def social_media_metrics(ig_url: str = None, fb_url: str = None, tiktok_url: str = None):
    """returns dictionary of facebook, instagram, and tiktok followers count.
    return None if no url or invalid url is found"""
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                              options=options)  # headless driver
    meta_metrics = {}

    print("Starting to scrape.....")

    if not ig_url:
        meta_metrics["instagram"] = None

    if not fb_url:
        meta_metrics["facebook"] = None

    if not tiktok_url:
        meta_metrics["tiktok"] = None

    if fb_url:
        fb_followers_count = facebook_followers(driver, fb_url)
        meta_metrics["facebook"] = fb_followers_count

    if ig_url:
        insta_followers_count = instagram_followers(driver, url=ig_url)
        meta_metrics["instagram"] = insta_followers_count

    if tiktok_url:
        tiktok_followers_count = tiktok_followers(driver, url=tiktok_url)
        meta_metrics["tiktok"] = tiktok_followers_count

    print("Done Scraping")
    driver.quit()
    return meta_metrics


if __name__ == "__main__":
    tiktok = "https://www.tiktok.com/@planetmoney"
    facebook_url = "https://web.facebook.com/YusufCatStevens/?_rdc=1&_rdr"
    instagram_url = "https://www.instagram.com/yusufcatstevens/"

    result = social_media_metrics(ig_url=instagram_url, fb_url=facebook_url, tiktok_url=tiktok)

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)
