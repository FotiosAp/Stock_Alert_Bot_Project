import datetime
import requests
import os
from dotenv import load_dotenv
load_dotenv()
ALPHA_VANTAGE_API_KEY=os.environ.get("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY=os.environ.get("NEWS_API_KEY")
BOT_TOKEN=os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID=os.environ.get("TELEGRAM_CHAT_ID")
ALERT_THRESHOLD=5
#COMMENT: CONFIGURATION CONSTANTS (Easily change the tracked stock or alert threshold)
STOCK = "TSLA"
COMPANY_NAME = "Tesla"
today_str = str(datetime.date.today())
yesterday_str = str(datetime.date.today() - datetime.timedelta(days=1))
day_before_yesterday_str=str(datetime.date.today() - datetime.timedelta(days=2))
today_weekday=(datetime.date.today()).weekday()
yesterday_weekday=(datetime.date.today()-datetime.timedelta(days=1)).weekday()
day_before_yesterday_weekday=(datetime.date.today()-datetime.timedelta(days=2)).weekday()
#STEP 1 - FETCH STOCK DATA FROM ALPHA VANTAGE
parameters_stock={
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK,
    "apikey":ALPHA_VANTAGE_API_KEY
}
response_stock=requests.get(url="https://www.alphavantage.co/query",params=parameters_stock)
response_stock.raise_for_status()
# print(response_stock.json())
data_stock=response_stock.json()
#Adjust the calculation days based on the current weekday to avoid weekend errors (markets are closed)
if today_weekday == 0:
    yesterday_price = float(data_stock["Time Series (Daily)"][str(datetime.date.today() - datetime.timedelta(days=3))]["4. close"])
    day_before_yesterday_price = float(data_stock["Time Series (Daily)"][str(datetime.date.today() - datetime.timedelta(days=4))]["4. close"])
elif today_weekday == 1:
    yesterday_price = float(data_stock["Time Series (Daily)"][str(datetime.date.today() - datetime.timedelta(days=1))]["4. close"])
    day_before_yesterday_price = float(data_stock["Time Series (Daily)"][str(datetime.date.today() - datetime.timedelta(days=4))]["4. close"])
elif today_weekday == 6:
    yesterday_price = float(data_stock["Time Series (Daily)"][str(datetime.date.today() - datetime.timedelta(days=2))]["4. close"])
    day_before_yesterday_price = float(data_stock["Time Series (Daily)"][str(datetime.date.today() - datetime.timedelta(days=3))]["4. close"])
else:
    yesterday_price = float(data_stock["Time Series (Daily)"][str(datetime.date.today() - datetime.timedelta(days=1))]["4. close"])
    day_before_yesterday_price = float(data_stock["Time Series (Daily)"][str(datetime.date.today() - datetime.timedelta(days=2))]["4. close"])
diff=((yesterday_price-day_before_yesterday_price)/day_before_yesterday_price)*100
diff=round(diff,2)
#STEP 2 - FETCH RELEVANT NEWS FROM NEWS API
parmeters_news={
    "q":COMPANY_NAME,
    "apiKey":NEWS_API_KEY,
    "from":day_before_yesterday_str,
    "to":today_str,
    "sortBy":"popularity",
    "searchIn":"title"
}
if diff>0:
    emoji="🔺"
elif diff<0:
    emoji="🔻"
else:
    emoji="-"

response_news=requests.get(url="https://newsapi.org/v2/everything",params=parmeters_news)
response_news.raise_for_status()
data_news=response_news.json()
#Slice the list to get only the top 3 articles
top_news_list=data_news["articles"][:3]
# print(top_news_list)
bot_token=BOT_TOKEN
#STEP 3 - FORMAT AND SEND TELEGRAM ALERT
url=f"https://api.telegram.org/bot{bot_token}/sendMessage"
if abs(diff)>=ALERT_THRESHOLD:
    for i in top_news_list:
        message_text = f"""
TSLA: {emoji}{abs(diff)}%
Headline: {i['title']}
Brief: {i['description']}
Link: {i['url']}"""
        payload = {
            "chat_id": CHAT_ID ,
            "text": message_text
        }
        telegram_message=requests.post(url=url,data=payload)
        telegram_message.raise_for_status()
    print("Message sent")
else:
    message_text = f"""
    TSLA: {emoji}{abs(diff)}%
Not big percentage change."""
    payload = {
        "chat_id": CHAT_ID,
        "text": message_text
    }
    telegram_message=requests.post(url=url,data=payload)
    telegram_message.raise_for_status()
    print("Message sent")
    # print(f"Not big percentage change: {diff}%")


