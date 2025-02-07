import tweepy
import os
from flask import Flask
import time

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

# מחלקה למעקב אחרי ציוצים
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            # מתעלם מציוצים של הבוט עצמו
            if status.user.id == api.verify_credentials().id:
                return
            
            # אם מישהו מצייץ על "תהילה"
            if "תהילה" in status.text:
                reply = f"@{status.user.screen_name} 'עוד יספרו לבנינו, על תהילת הימים!'"
                api.update_status(
                    status=reply,
                    in_reply_to_status_id=status.id
                )
                print(f"הגבתי לציוץ: {status.text}")
                
        except Exception as e:
            print(f"שגיאה: {e}")

@app.route('/')
def home():
    return "הבוט רץ! מחפש ציוצים על תהילה..."

def start_stream():
    try:
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.filter(track=['תהילה'], languages=['he'], is_async=True)
    except Exception as e:
        print(f"שגיאה בהפעלת הסטרים: {e}")

if __name__ == "__main__":
    start_stream()  # מתחיל את המעקב אחרי ציוצים
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
    
