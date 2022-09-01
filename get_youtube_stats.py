from googleapiclient.discovery import build
import os

youtube_api = os.environ.get("YOUTUBE_API_KEY")
youtube_service = build("youtube", "v3", developerKey=youtube_api)


def get_youtube_metrics(channel_url: str = None):
    """takes artist channel url and return dict of channel stats or None if no url is provided"""
    if not channel_url:
        return None
    if "channel" not in channel_url:
        print("please provide a music channel url")
        return None
    try:
        channel_id = channel_url.strip('/').split('/')[-1]
        request = youtube_service.channels().list(part="statistics,snippet", id=channel_id)
        response = request.execute()
        stats = response["items"][0]["statistics"]
        return {"view_count": int(stats["viewCount"]), "subscriber_count": int(stats["subscriberCount"])}

    except Exception as e:
        print(f"an error occurred while fetching channel stats: \n{e}")
        return None


if __name__ == "__main__":
    r = get_youtube_metrics("https://www.youtube.com/channel/UC3lnDRwdK-CD2xjO-16zmmg")
    print(r)
