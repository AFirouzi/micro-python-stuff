import tweepy
from datetime import datetime
from urllib import request

### Tokens
auth = tweepy.OAuthHandler(
    "AP_KEY", "API_SECRET_KEY"
)
auth.set_access_token(
    "Access Token",
    "Access Token Secret",
)
### Tokens
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

class Video():
    def __init__(self,bitrate,url):
        self.bitrate = bitrate
        self.url = url
        self.size = round(request.urlopen(url=url).length / 1024)
        self.size_note = "kb"
        self.dimensions = str(url).split("/")[-2]
        self.ErrorCode = -1
        if self.size > 1000:
            self.size = round(self.size / 1024, 1)
            self.size_note = "mb"

def return_video(tweet_url):
    url = str(tweet_url)
    if url.strip() == "":
        raise ValueError("Invalid URL: " + url)
    if "https://twitter.com/" not in url.strip():
        raise ValueError("Invalid URL")
    try:
        status = api.get_status(id=url.split(sep="/")[-1], tweet_mode="extended")
    except tweepy.TweepError as twe:
        if(twe.api_code == 179):
            raise ValueError(str(179))
    
    video_list = status.extended_entities["media"][0]["video_info"]["variants"]
    result_list = []
    extra_info = dict()    
    extra_info["text"] = str(status.full_text).split("https://t.co")[0]
    extra_info["tweet_link"] = (
        "https://t.co" + str(status.full_text).split("https://t.co")[1]
    )
    extra_info["author"] = (
        str(status.user.screen_name) + "(" + str(status.user.name) + ")"
    )

    for item in video_list:
        if "bitrate" in item:
            video = Video(str(item["bitrate"]),str(item["url"]))
            result_list.append(video)
    return (result_list,extra_info)
