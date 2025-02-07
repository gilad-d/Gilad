import tweepy
import os
from flask import Flask
from threading import Thread

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

class MyStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        try:
            print(f"מצאתי ציוץ: {tweet.text}")
            
            if "תהילה" in tweet.text:
                reply = f"@{tweet.author.username} 'עוד יספרו לבנינו, על תהילת הימים!'"
                api.update_status(
                    status=reply,
                    in_reply_to_status_id=tweet.id
                )
                print(f"הגבתי לציוץ: {tweet.text}")
                
        except Exception as e:
            print(f"שגיאה: {e}")
            print(f"פרטי השגיאה המלאים: {str(e)}")

def run_stream():
    print("מתחיל להאזין לציוצים...")
    try:
        stream = MyStream(bearer_token=os.environ.get('TWITTER_BEARER_TOKEN'))
        stream.filter(track=['תהילה'], languages=['he'])
    except Exception as e:
        print(f"שגיאה בהפעלת הסטרים: {e}")

@app.route('/')
def home():
    print("מישהו ביקר בדף הבית של הבוט!")
    return "הבוט רץ! מחפש ציוצים על תהילה..."

if __name__ == "__main__":
    # מפעיל את הstream בthread נפרד
    stream_thread = Thread(target=run_stream)
    stream_thread.daemon = True
    stream_thread.start()
    
    # מפעיל את השרת
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
