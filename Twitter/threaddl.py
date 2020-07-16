import twint
import tweepy
import datetime
import pandas

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

# Get a tweet from the thread
# You can get TWEET_ID from tweet url ex: https://twitter.com/Twitter/status/1278347468690915330
# TWEET_ID = 1278347468690915330
status = api.get_status(id="TWEET_ID", tweet_mode="extended")

username = status.user.screen_name
thread = []

# Find the first tweet of the thread
while status.in_reply_to_status_id_str != None:
    status = api.get_status(id=status.in_reply_to_status_id_str, tweet_mode="extended")

cur_tweet_id = status.id_str
cur_tweet_text = status.full_text
thread.append(cur_tweet_text + '\n')

# Using Twint to scrap tweets and bypass the limitaion of Twitter API
c = twint.Config()
c.Username = username
c.To = username
c.Since = str(datetime.datetime.strptime(str(status.created_at), '%Y-%m-%d %H:%M:%S').date())
c.Pandas = True
c.Hide_output = True
twint.run.Search(c)

Tweets_df = twint.storage.panda.Tweets_df
Tweets_df = Tweets_df[['id','created_at','tweet','user_id','conversation_id']]
Tweets_df.sort_values(by=['id'])

# Each tweet in twint has a conversation_id. you find it, you can find all of the tweets that belong to that thread.
conversation_id = None
for index, row in Tweets_df.iterrows():
    status = api.get_status(id=row['id'], tweet_mode="extended")
    if status.in_reply_to_status_id_str == cur_tweet_id:
        conversation_id = row['conversation_id']
        
# Reordering tweets
Tweets_df = Tweets_df.loc[Tweets_df['conversation_id'] == conversation_id].iloc[::-1]
thread += (Tweets_df['tweet'] + '\n').tolist()

# writing the thread on the file
open("thread.txt","w+",encoding='utf-8').writelines(thread)
