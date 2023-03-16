from openweather import OpenWeatherAPI
from requests import Request, Session
from requests_cache import CachedSession
import numpy as np
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
        owAPI.forecast1(city["lat"], city["lon"], units="metric").prepare()
    ).json()

    today_data = r["list"][:8]  # uses the next 8 forecasts, covering the next 24 hours
    temp_min = min(float(x["main"]["temp_min"]) for x in today_data)
    temp_max = max(float(x["main"]["temp_max"]) for x in today_data)

    icon_infos = [get_weather_info(x["weather"][0]["icon"]) for x in today_data]
    values = [x["value"] for x in icon_infos]
    avg_value = average(values, e=2)
    emoji = nearest_icon(avg_value)[1]["emoji"]
    print([x["emoji"] for x in icon_infos])
    print(avg_value, emoji)

    temps = " / ".join(f"{t:.1f}°" for t in [temp_min, temp_max])
    message = f'{city["name"]} {temps} {emoji}'
    return message


# see https://openweathermap.org/weather-conditions
with open("openweather-icons-info.json") as f:
    weather_icon_infos = json.load(f)

for icon, data in weather_icon_infos.items():
    data["value"] = np.array(data["value"])


def get_weather_info(weather_icon):
    return weather_icon_infos[weather_icon[:2]]


def old_average(values, e=1):
    k = len(values[0])
    sums = [0 for _ in range(k)]
    for v in values:
        for i in range(k):
            x = abs(v[i] ** e)
            if v[i] < 0:
                x = -x
            sums[i] += x

    avg = [None for _ in range(k)]
    for i in range(k):
        x = abs(sums[i] / len(values)) ** (1 / e)
        if sums[i] < 0:
            x = -x
        avg[i] = x

    return avg


def average(values, e=1):
    values = np.array(values)
    powers = np.float_power(abs(values), e) * np.sign(values)
    mean_powers = np.mean(powers, axis=0)
    return np.float_power(abs(mean_powers), 1 / e) * np.sign(mean_powers)


def distance(x, y, e=2):
    # r = sum((a - b) ** e for a, b in zip(x, y))
    r = np.float_power(abs(x - y), e).sum()
    return r


def nearest_icon(avg_value):
    return min(
        weather_icon_infos.items(), key=lambda kv: distance(avg_value, kv[1]["value"])
    )


OPEN_WEATHER_API_KEY = os.environ["OPEN_WEATHER_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHATS_ID = os.environ["TELEGRAM_CHATS_ID"].split()

cities = {("Catania", "IT"): None, ("Udine", "IT"): None}


owAPI = OpenWeatherAPI(OPEN_WEATHER_API_KEY)
owSession = CachedSession("ow_cache", cache_control=True)

for name_country in cities:
    r = owSession.send(owAPI.direct_geocoding(*name_country).prepare()).json()
    cities[name_country] = r[0]

message = "\n".join(city_message(city) for city in cities.values())

bot = telegram.Bot(TELEGRAM_TOKEN)
for chat_id in TELEGRAM_CHATS_ID:
    asyncio.run(bot.send_message(text=message, chat_id=chat_id))
