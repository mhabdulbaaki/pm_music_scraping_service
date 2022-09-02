from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from get_spotify_data import artist_spotify_data
from get_twitter_followers import twitter_followers_count
from get_youtube_stats import get_youtube_metrics
from scrape_social_platforms import tiktok_followers, facebook_followers, instagram_followers
import pprint

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')


def get_artist_stats(spotify_url: str, fb: str = None, tiktok: str = None,
                     twitter: str = None, instagram: str = None,
                     youtube: str = None, twitter_handle: str = None):
    """ returns the artist stats across different platforms"""

    try:
        # get spotify data
        spotify_data = artist_spotify_data(url=spotify_url)

        fb_url = spotify_data.pop("facebook") if not fb else fb
        twitter_url = spotify_data.pop("twitter") if not twitter else twitter
        instagram_url = spotify_data.pop("instagram") if not instagram else instagram

        # install & initialize chrome webdriver
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                  options=options)  # headless driver

        # twitter stats
        twitter_data = twitter_followers_count(url=twitter_url, artist_twitter_handle=twitter_handle)

        # facebook
        facebook_data = facebook_followers(driver=driver, url=fb_url)

        # instagram
        instagram_data = instagram_followers(driver=driver, url=instagram_url)

        # YouTube stats
        youtube_data = get_youtube_metrics(channel_url=youtube)

        # get tiktok facebook and instagram
        tiktok_data = tiktok_followers(driver=driver, url=tiktok)

        driver.quit()  # quit driver
        return {
            "spotify_data": spotify_data,
            "twitter_data": twitter_data,
            "facebook_data": facebook_data,
            "tiktok_data": tiktok_data,
            "instagram_data": instagram_data,
            "youtube_data": youtube_data
        }
    except Exception as e:
        print(f"an error occurred while fetching artist stats: \n {e}")
        return None


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=2)
    r = get_artist_stats(spotify_url="https://open.spotify.com/artist/01DTVE3KmoPogPZaOvMqO8")
    pp.pprint(r)
