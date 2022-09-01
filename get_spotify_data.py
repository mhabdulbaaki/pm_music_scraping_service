from search_artist_on_spotify import spotify_search_artist
from scrape_spotify_top_streams import artist_top_stream_songs
import pprint

pretty_print = pprint.PrettyPrinter(indent=2)


def artist_spotify_data(name: str):
    """ takes artist name and returns dictionary containing artist information on spotify"""

    artist_data = spotify_search_artist(name=name)
    url = artist_data["spotify_page"]
    artist_data["most_stream_songs"] = artist_top_stream_songs(url)
    return artist_data


if __name__ == "__main__":
    artist_info = artist_spotify_data(name="jay ghartey")
    pretty_print.pprint(artist_info)
