import tweepy
import os
from flask import Flask

app = Flask(__name__)

# Twitter API הגדרות
auth = tweepy.OAuthHandler(
    os.environ.get('TWITTER_API_KEY'),
    os.environ.get('TWITTER_API_SECRET')
)
auth.set_access_token(
    os.environ.get('TWITTER_ACCESS_TOKEN'),
    os.environ.get('TWITTER_ACCESS_SECRET')
)

api = tweepy.API(auth)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
