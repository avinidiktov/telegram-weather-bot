from src.weather.weather import Weather
from src.constants import constants

weater = Weather(constants.DARK_SKY_API_KEY)

print(weater.get_current_forecast(('Ulan Bator')))
