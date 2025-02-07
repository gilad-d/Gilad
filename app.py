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
    print("בודק אם הבוט עובד...")
    try:
        # בדיקה שהחיבור לטוויטר עובד
        api.verify_credentials()
        print("החיבור לטוויטר עובד!")
        
        # ניסיון לצייץ
        api.update_status("בדיקה - הבוט פעיל!")
        print("הצלחתי לצייץ!")
        
        return "הבוט עובד! בדוק את הציוץ החדש בחשבון שלך."
    except Exception as e:
        print(f"שגיאה: {str(e)}")
        return f"יש שגיאה: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
