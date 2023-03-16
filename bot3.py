from openweather import OpenWeatherAPI
from requests import Request, Session
from requests_cache import CachedSession
import telegram
import asyncio
from datetime import date
import json
import os
import pprint as _pprint


## custom pretty printer
_pretty_printer = _pprint.PrettyPrinter(sort_dicts=False)
pprint = _pretty_printer.pprint


## constructs a message about a city's weather
def city_message(city):
    r = owSession.send(
        owAPI.onecall(
            lat=city["lat"],
            lon=city["lon"],
            units="metric",
            exclude="current,minutely,hourly",
        ).prepare()
    ).json()
    today_data = r["daily"][0]

    temps = (today_data["temp"][key] for key in ["min", "max"])
    temps_string = " / ".join(f"{t:.1f}°" for t in temps)

    emoji = get_weather_emoji(today_data["weather"][0]["icon"])
    message = f'{city["name"]} {temps_string} {emoji}'

    return message


# see https://openweathermap.org/weather-conditions
with open("openweather-icons-info.json") as f:
    weather_icon_infos = json.load(f)


def get_weather_info(weather_icon):
    return weather_icon_infos[weather_icon[:2]]


def get_weather_emoji(weather_icon):
    return get_weather_info(weather_icon)["emoji"]


OPEN_WEATHER_API_KEY = os.environ["OPEN_WEATHER_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHATS_ID = os.environ["TELEGRAM_CHATS_ID"].split(",")

cities = {("Catania", "IT"): None, ("Udine", "IT"): None}


owAPI = OpenWeatherAPI(OPEN_WEATHER_API_KEY)
owSession = CachedSession("ow_cache", cache_control=True)

for name_country in cities:
    r = owSession.send(owAPI.direct_geocoding(*name_country).prepare()).json()
    cities[name_country] = r[0]

message = "\n".join(city_message(city) for city in cities.values())

async def main():
    bot = telegram.Bot(TELEGRAM_TOKEN)
    for chat_id in TELEGRAM_CHATS_ID:
        await bot.send_message(text=message, chat_id=chat_id)

asyncio.run(main())
