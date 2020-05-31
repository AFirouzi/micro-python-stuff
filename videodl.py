import tweepy
import wget
from datetime import datetime

###Keys & Tokens
auth = tweepy.OAuthHandler(
    "AP_KEY", "API_SECRET_KEY"
)
auth.set_access_token(
    "Access Token",
    "Access Token Secret",
)
###Keys & Tokens
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def download_video(url, quality):
    """
    Takes url of the tweet and Quality you prefer.
    quality="H" means high quality
    quality="M" means medium quality
    quality="L" means low quality

    """
    url = str(url)
    if url.strip() == "":
        raise ValueError("Invalid URL")
    if "https://twitter.com/" not in url.strip():
        raise ValueError("Invalid URL")
    status = api.get_status(id=url.split(sep="/")[-1], tweet_mode="extended")
    title = "video_" + (datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    if "title" in str(status.extended_entities["media"][0]["additional_media_info"]):
        title = (
            str(status.extended_entities["media"][0]["additional_media_info"]["title"])
            + "_"
            + (datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        )
    video_list = status.extended_entities["media"][0]["video_info"]["variants"]
    video_url = ""
    for item in video_list:
        if 'bitrate' in item and int(item['bitrate']) == 432000 and quality == "L":
            video_url = str(item["url"])
            title += "_LQ"
        if 'bitrate' in item and int(item['bitrate']) == 832000 and quality == "M":
            video_url = str(item["url"])
            title += "_MQ"
        if 'bitrate' in item and int(item['bitrate']) == 1280000 and quality == "H":
            video_url = str(item["url"])
            title += "_HQ"
    if video_url == "":
        print("Video with given quality can't be found")
    else:
        print("\nDownloading " + title + " ...")
        wget.download(video_url, out=title + ".mp4")