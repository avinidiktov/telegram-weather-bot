from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging

from src.weather.weather import Weather
from src.constants import constants


weater = Weather(constants.DARK_SKY_API_KEY)
updater = Updater(token=constants.TELEGRAM_BOT_TOKEN)
dispatcher = updater.dispatcher

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Hello! It's weather X bot. For to get weather" +
                     "information, enter the name of needed location." +
                     "For example \"Ulan Bator\".")


def get_current_forecast(bot, update):
    forecast = weater.get_current_forecast(update.message.text)
    bot.send_message(chat_id=update.message.chat_id,
                     text=("%.1f °C" % forecast["temperature"]))


start_handler = CommandHandler("start", start)
forecast_handler = MessageHandler(Filters.text, get_current_forecast)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(forecast_handler)

updater.start_polling()
