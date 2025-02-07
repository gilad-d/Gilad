import tweepy
import os
import time
from flask import Flask
from threading import Thread
import random
import logging

# הגדרת logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    "דגון - אל הדגן"
]

def post_god():
    logger.info("Thread של הציוצים התחיל!")
    while True:
        try:
            # בחירת אל רנדומלי
            god = random.choice(canaanite_gods)
            logger.info(f"מנסה לצייץ על: {god}")
            
            # בדיקת חיבור לטוויטר
            logger.info("בודק חיבור לטוויטר...")
            api.verify_credentials()
            logger.info("החיבור לטוויטר תקין")
            
            # פרסום הציוץ
            status = api.update_status(god)
            logger.info(f"הציוץ פורסם בהצלחה! ID: {status.id}")
            
            # חכה 10 דקות
            logger.info("מחכה 10 דקות...")
            time.sleep(600)
            
        except Exception as e:
            logger.error(f"שגיאה בפרסום: {str(e)}")
            time.sleep(60)  # אם יש שגיאה, חכה דקה ונסה שוב

@app.route('/')
def home():
    logger.info("מישהו ביקר בדף הבית")
    return "הבוט רץ! מצייץ על אלים כנעניים כל 10 דקות."

if __name__ == "__main__":
    logger.info("האפליקציה מתחילה...")
    
    # הפעל את הפרסום התקופתי בthread נפרד
    try:
        poster_thread = Thread(target=post_god)
        poster_thread.daemon = True
        poster_thread.start()
        logger.info("Thread של הציוצים הופעל בהצלחה")
    except Exception as e:
        logger.error(f"שגיאה בהפעלת Thread: {str(e)}")
    
    # הפעל את השרת
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
