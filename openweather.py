from requests import Request, Session

## OpenWeather API wrapper
class OpenWeatherAPI:
    base_url = "https://api.openweathermap.org"

    def __init__(self, key):
        self.key = key

    ## returns a requests.Request; usage: response = session.send(request.prepare())
    def request(self, url, **params):
        params["appid"] = self.key
        return Request("GET", self.base_url + "/" + url, params=params)

    ## Direct geocoding: converts the specified name of a location or
    ## zip/post code into the exact geographical coordinates
    ## (https://openweathermap.org/api/geocoding-api)
    def direct_geocoding(self, city_name, country_code, state_code=None, limit=None):
        if state_code is not None:
            query = [city_name, state_code, country_code]
        else:
            query = [city_name, country_code]

        params = {"q": ",".join(query)}
        if limit is not None:
            params["limit"] = limit

        return self.request("geo/1.0/direct", **params)

    ## Call 5 day / 3 hour forecast data (https://openweathermap.org/forecast5)
    def forecast1(self, lat, lon, **params):
        return self.request("data/2.5/forecast", lat=lat, lon=lon, **params)

    ## Call 16 day / daily forecast data, non-Free (https://openweathermap.org/forecast16)
    def forecast_daily(self, **params):
        return self.request("data/2.5/forecast/daily", **params)

    ## One Call API 3.0 (https://openweathermap.org/api/one-call-3)
    def onecall(self, lat, lon, **params):
        return self.request("data/3.0/onecall", lat=lat, lon=lon, **params)

    def onecall_timemachine(self, lat, lon, dt, **params):
        return self.request("data/3.0/onecall/timemachine", lat=lat, lon=lon, dt=dt, **params)
