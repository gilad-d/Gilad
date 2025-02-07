import tweepy
import os
from flask import Flask

app = Flask(__name__)

# הגדרות Twitter API
auth = tweepy.OAuthHandler(
    os.environ.get('TWITTER_API_KEY'),
    os.environ.get('TWITTER_API_SECRET')
)
auth.set_access_token(
    os.environ.get('TWITTER_ACCESS_TOKEN'),
    os.environ.get('TWITTER_ACCESS_SECRET')
)

api = tweepy.API(auth)

# הגרסה החדשה משתמשת ב-StreamingClient במקום StreamListener
class MyStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        try:
            # מתעלם מציוצים של הבוט עצמו
            if tweet.author_id == api.verify_credentials().id:
                return
            
            # אם מישהו מצייץ על "תהילה"
            if "תהילה" in tweet.text:
                reply = f"@{tweet.author.username} 'עוד יספרו לבנינו, על תהילת הימים!'"
                api.update_status(
                    status=reply,
                    in_reply_to_status_id=tweet.id
                )
                print(f"הגבתי לציוץ: {tweet.text}")
                
        except Exception as e:
            print(f"שגיאה: {e}")

@app.route('/')
def home():
    return "הבוט רץ! מחפש ציוצים על תהילה..."

def start_stream():
    try:
        # שים לב שכאן צריך את ה-Bearer Token במקום OAuth
        stream = MyStream(bearer_token=os.environ.get('TWITTER_BEARER_TOKEN'))
        stream.filter(track=['תהילה'], languages=['he'])
    except Exception as e:
        print(f"שגיאה בהפעלת הסטרים: {e}")

if __name__ == "__main__":
    start_stream()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
    
