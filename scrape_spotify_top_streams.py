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


def artist_top_stream_songs(url: str):
    """
    takes a spotify artist url
    returns a list of 10 most stream songs
    returns None if error occurs
    """
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                              options=options)  # headless driver
    driver.get(url)

    # xpath to 'see more' text button
    x_path = ("//*[@id='main']/div/div[2]/div[3]/div[1]/"
              "div[2]/div[2]/div/div/div[2]/main/section/div/"
              "div[2]/div[3]/div[1]/div/div/button/div")

    body_html = driver.find_element(By.TAG_NAME, "html")

    try:
        # click see more button
        # driver.execute_script("arguments[0].click();",driver.find_element(By.XPATH, x_path))
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 5).
                              until(ec.element_to_be_clickable((By.XPATH, x_path))))

        html = body_html.get_attribute('outerHTML')

        time.sleep(2)
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all(attrs={"data-testid": "tracklist-row"})

        most_stream_songs = []
        for row in rows:
            song_title = row.contents[1].get_text()
            stream_count = int(row.contents[2].get_text().replace(",", ""))

            most_stream_songs.append({song_title: stream_count})

        # close drive
        driver.quit()

        return most_stream_songs

    except Exception as e:
        print(e)

        driver.quit()
        return None


if __name__ == "__main__":
    r = artist_top_stream_songs(url="https://open.spotify.com/artist/7ijkc3O3uxDdAmSuQUg2f2")
    print(f"result: \n{r}")
