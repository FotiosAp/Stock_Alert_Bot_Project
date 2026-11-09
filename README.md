# Stock Alert Bot

An automated Python script that monitors daily stock price fluctuations (e.g., Tesla) and sends real-time alerts to a Telegram chat. If the stock price changes by a specified percentage threshold, the bot automatically fetches the top related news articles and delivers them straight to your phone.

## Key Features

- **Automated Data Fetching:** Uses the Alpha Vantage API to retrieve daily stock closing prices.
- **Smart Weekend Logic:** Automatically adjusts the calculation days based on the current weekday to avoid errors when stock markets are closed.
- **News Integration:** Connects to the News API to pull the top 3 most relevant articles when a significant price change is detected.
- **Instant Notifications:** Sends formatted alerts with price change percentages, emojis (🔺/🔻), and news links directly via Telegram.
- **Secure Configuration:** Protects sensitive API keys and tokens by pulling them from a local `.env` environment variables file.

## System Requirements

- Python 3.x
- `requests` library (`pip install requests`)
- `python-dotenv` library (`pip install python-dotenv`)

## Setup & Installation

1. Create a file named `.env` in the root directory (same folder as `main.py`).
2. Add your API keys and credentials inside the `.env` file using the following format:

   ```env
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
   NEWS_API_KEY=your_news_api_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
