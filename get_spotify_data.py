from search_artist_on_spotify import spotify_search_artist
from scrape_spotify_top_streams import artist_top_stream_songs
from scrape_artist_media_handles_from_spotify import get_artist_media_handles
import pprint

pretty_print = pprint.PrettyPrinter(indent=2)


def artist_spotify_data(name: str = None, url: str = None):
    """ takes artist name and returns dictionary containing artist information on spotify"""

    artist_data = spotify_search_artist(name=name, url=url)
    url = artist_data["spotify_page"]
    artist_data["most_stream_songs"] = artist_top_stream_songs(url)
    artist_media_handles = get_artist_media_handles(spotify_url=url)

    return {**artist_data, **artist_media_handles}


if __name__ == "__main__":
    artist_info = artist_spotify_data(name="jay ghartey")
    pretty_print.pprint(artist_info)
