import requests
import os
import base64
import pprint

pretty_print = pprint.PrettyPrinter(indent=2)

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")


def spotify_access_token(client_id: str, client_secret: str) -> str:
    """
    client_id: client id from your spotify app
    client_secret: client scret generated from your spotify app dashboard

    returns a spotify access token
    """

    token_base_url = "https://accounts.spotify.com/api/token"

    client_credentials = f"{client_id}:{client_secret}"
    encode_client_cred = client_credentials.encode()
    base64_bytes = base64.b64encode(encode_client_cred)
    base64_message = base64_bytes.decode()

    token_payload = {"grant_type": "client_credentials"}
    token_headers = {"Authorization": f"Basic {base64_message}", "Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(token_base_url, data=token_payload, headers=token_headers)

    return response.json()["access_token"]


def spotify_search_artist(name: str = None, url: str = None, limit=1):
    """
    name: name of artist to search
    url: the spotify url of the artist e.g https://open.spotify.com/artist/5OC5mCMdUlT4F8H9knv2AD
    limit: maximum number of search results to return. default is 1 and maximum 10
    note spotify maximum limit is 50, but for our purpose 10 is enough
    """

    # reset limit to maximum
    if limit > 10:
        limit = 10

    # return None if both name and url are None
    if not name and not url:
        return None
    # access token
    access_token = spotify_access_token(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)

    # request headers
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {access_token}"
    }

    if url:
        channel_id = url.strip("/").split("/")[-1]
        base_url = f"https://api.spotify.com/v1/artists/{channel_id}"

        response = requests.get(base_url, headers=headers)

        if response.status_code != 200:
            print(f"an error occurred: \n{response.json()}")

        else:
            data = response.json()
            artist_info = {
                "spotify_page": data["external_urls"]["spotify"],
                "followers_count": data["followers"]["total"],
                "id": data["id"],
                "name": data["name"],
                "popularity": data["popularity"],
                "profile_image": data["images"][0]["url"],
            }

            return artist_info

    if name:
        search_base_url = "https://api.spotify.com/v1/search"

        # get request region
        region_res = requests.get("https://ipinfo.io/")
        region = region_res.json()["country"]

        # search parameters
        params = {
            "q": name,
            "type": "artist",
            "limit": limit,
            "market": region
        }

        response = requests.get(search_base_url, params=params, headers=headers)

        if response.status_code != 200:
            print(f"an error occurred: \n{response.json()}")

        else:
            if limit == 1:
                data = response.json()["artists"]["items"][0]
                artist_info = {
                    "spotify_page": data["external_urls"]["spotify"],
                    "followers_count": data["followers"]["total"],
                    "id": data["id"],
                    "name": data["name"],
                    "popularity": data["popularity"],
                    "profile_image": data["images"][0]["url"],
                }
                return artist_info
            else:
                artists_data = []
                for i in range(limit):
                    data = response.json()["artists"]["items"][i]
                    artist_info = {
                        "spotify_page": data["external_urls"]["spotify"],
                        "followers_count": data["followers"]["total"],
                        "id": data["id"],
                        "name": data["name"],
                        "popularity": data["popularity"],
                        # "profile_image": data["images"][0]["url"],
                    }
                    artists_data.append(artist_info)
                return artists_data


if __name__ == "__main__":
    # r = spotify_search_artist(url="https://open.spotify.com/artist/5OC5mCMdUlT4F8H9knv2AD")
    r = spotify_search_artist(name="sarkodie")
    pretty_print.pprint(r)
