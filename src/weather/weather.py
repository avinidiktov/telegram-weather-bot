from geopy.geocoders import Nominatim
import forecastio


def replace_icon_to_emoji(icon):
    """ Replace ForecastioDataPoint.icon string to emoji string

        icon -> class forecastio.models.ForecastioDataPoint.icon

    """
    return {
        "clear-day": ":sunny:",
        "clear-night": ":night_with_stars:",
        "rain": ":umbrella: :droplet:",
        "snow": ":snowflake: :snowman:",
        "sleet": ":snowflake: :droplet:",
        "wind": ":wind_blowing_face:",
        "fog": ":fog: :foggy:",
        "cloudy": ":cloud:",
        "partly-cloudy-day": ":white_sun_with_small_cloud:",
        "partly-cloudy-night": ":night_with_stars: :cloud:"
    }.get(icon, ":earth_asia:")


class Weather:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_current_forecast(self, area):
        geolocator = Nominatim()
        location = geolocator.geocode(area)
        forecast = forecastio.load_forecast(
            self.api_key, location.latitude, location.longitude, units="si")

        return {
            "summary": forecast.currently().summary,
            "temperature": forecast.currently().temperature,
            "emoji": replace_icon_to_emoji(forecast.currently().icon)
        }
