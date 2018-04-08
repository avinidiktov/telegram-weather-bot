from geopy.geocoders import Nominatim
import forecastio


class Weather:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_current_forecast(self, area):
        geolocator = Nominatim()
        location = geolocator.geocode(area)
        forecast = forecastio.load_forecast(
            self.api_key, location.latitude, location.longitude)

        return (forecast.currently().summary, forecast.currently()
                .temperature, forecast.currently().icon)
