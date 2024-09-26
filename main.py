import requests
from twilio.rest import Client


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
account_sid = "AC9199207ce7e3aa2f74311c9fda98ee17"
auth_token = "5d954351ecdd74375a362ab868d56021"


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API = "0SDKKUYSFBU4V5YB"
NEWS_API = "bd2e2242fd474859932c8f8e0b579868"


stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_close = yesterday_data["4. close"]
print(yesterday_close)

day_before = data_list[1]
day_before_close = day_before["4. close"]
print(day_before_close)


difference = (float(yesterday_close) - float(day_before_close))
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"


diff_percentage = round((difference/float(yesterday_close)) * 100)
print(diff_percentage)


if abs(diff_percentage) > 1:
    news_params = {
        "apiKey": NEWS_API,
        "qInTitle": COMPANY_NAME,

    }
    news_response = requests.get(NEWS_ENDPOINT, params= news_params)
    articles = (news_response.json()["articles"])

    three_articles = articles[:3]
    #print(three_articles)

    formatted_article = [f"{STOCK_NAME}: {up_down}{diff_percentage}% Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]


    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=formatted_article,
        from_="+12052369996",
        to="+919148728492"
    )

#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

