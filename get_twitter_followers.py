import requests
import os

API_KEY = os.environ.get("TWITTER_API_KEY_MUSIC")
API_SECRET = os.environ.get("TWITTER_API_KEY_SECRET_MUSIC")


# get bearer token
def create_bearer_token_url():
    return 'https://api.twitter.com/oauth2/token'


def get_bearer_params():
    return {'grant_type': 'client_credentials'}


def bearer_auth():
    return f'{API_KEY}', f'{API_SECRET}'


def get_twitter_access_token(url: str, params: dict):
    response = requests.post(url, params=params, auth=bearer_auth())

    if response.status_code != 200:
        raise Exception(
            f"Request returned an error: {response.status_code} {response.text}"
        )
    return response.json()['access_token']


def create_metrics_url(user_name: str):
    return f"https://api.twitter.com/2/users/by/username/{user_name}"


def get_metrics_params():
    return {'user.fields': 'public_metrics'}


def get_metrics_headers(bearer_token: str):
    return {'Authorization': f"Bearer {bearer_token}"}


def get_public_metrics(url: str, headers: dict, params: dict):
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(
            f"Request returned an error: {response.status_code} {response.text}"
        )
    return response.json()


def twitter_followers_count(artist_twitter_handle: str = None, url: str = None):
    """takes user twitter handle [e.g @mhabdulbaaki] and returns the followers count for the user"""

    # return None if both url & handle are none
    if not artist_twitter_handle and not url:
        return None

    # strip @ sign of handle
    if artist_twitter_handle and "@" in artist_twitter_handle:
        artist_twitter_handle = artist_twitter_handle.lstrip("@")

    # get handle from url
    if url:
        artist_twitter_handle = url.strip("/").split("/")[-1]

    try:
        # get bearer tokens
        bearer_token_url = create_bearer_token_url()
        bearer_url_params = get_bearer_params()
        bearer_token = get_twitter_access_token(url=bearer_token_url, params=bearer_url_params)

        # get public metrics
        metrics_url = create_metrics_url(user_name=artist_twitter_handle)
        metrics_params = get_metrics_params()
        metrics_headers = get_metrics_headers(bearer_token=bearer_token)

        json_response = get_public_metrics(url=metrics_url, headers=metrics_headers, params=metrics_params)
        return {"followers_count": json_response["data"]["public_metrics"]["followers_count"]}
    except Exception as e:
        print(f"an error occurred while fetching twitter followers count: \n{e}")
        return None


if __name__ == "__main__":
    r = twitter_followers_count(artist_twitter_handle="@mhabdulbaaki")
    print(r)
