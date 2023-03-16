# weatherbot
Just a Telegram bot that sends daily notifications about weather forecast for personal need. Nothing fancy. 

### Usage
Install dependecies with `pip3 install requirements.txt`. 
Run `python3 bot3.py` or `python3 bot.py` in an environment where the following variables are defined:
- `OPEN_WEATHER_API_KEY` (see https://openweathermap.org/api) 
- `TELEGRAM_TOKEN` (see https://core.telegram.org/bots/api)
- `TELEGRAM_CHATS_ID`: a comma separated list of Telegram chat IDs

Note:
- `bot3.py` uses (One Call API 3.0)[https://openweathermap.org/api/one-call-3] with "One Call by Call" subscription plan (recommended option)
- `bot.py` uses the Professional API collections with different fixed-price subscriptions (see (princing)[https://openweathermap.org/price]); a free plan is available  

