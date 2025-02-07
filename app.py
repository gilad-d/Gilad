import tweepy
import os
import time
from flask import Flask
from threading import Thread
import random

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

# רשימת אלים כנעניים
canaanite_gods = [
    "בעל - אל הסערה והפוריות",
    "ענת - אלת המלחמה והאהבה",
    "אשרה - אלת הים והפוריות",
    "דגון - אל הדגן",
    "מות - אל המוות",
    "שמש - אל השמש",
    "ירח - אל הירח",
    "רשף - אל המגפות והמלחמה",
    "חורון - אל המאגיה השחורה",
    "קדש - אלת הקדושה",
    "מלקרת - אל העיר צור"
]

def post_god():
    while True:
        try:
            # בחירת אל רנדומלי
            god = random.choice(canaanite_gods)
            print(f"מנסה לצייץ על: {god}")
            
            # פרסום הציוץ
            api.update_status(god)
            print("הציוץ פורסם בהצלחה!")
            
            # חכה 10 דקות
            time.sleep(600)
            
        except Exception as e:
            print(f"שגיאה בפרסום: {str(e)}")
            time.sleep(60)  # אם יש שגיאה, חכה דקה ונסה שוב

@app.route('/')
def home():
    return "הבוט רץ! מצייץ על אלים כנעניים כל 10 דקות."

if __name__ == "__main__":
    # הפעל את הפרסום התקופתי בthread נפרד
    poster_thread = Thread(target=post_god)
    poster_thread.daemon = True
    poster_thread.start()
    
    # הפעל את השרת
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
