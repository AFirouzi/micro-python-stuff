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
    if quality == "H":
        video_url = str(
            status.extended_entities["media"][0]["video_info"]["variants"][2]["url"]
        )
        title += "_HQ"
    if quality == "M":
        video_url = str(
            status.extended_entities["media"][0]["video_info"]["variants"][0]["url"]
        )
        title += "_MQ"
    if quality == "L":
        video_url = str(
            status.extended_entities["media"][0]["video_info"]["variants"][1]["url"]
        )
        title += "_LQ"
    print("\nDownloading " + title + " ...")
    wget.download(video_url, out=title + ".mp4")
