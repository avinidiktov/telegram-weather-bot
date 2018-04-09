import time
import os

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from emoji import emojize
import logging

from src.weather.weather import Weather


weater = Weather(os.environ.get('DARK_SKY_API_KEY'))
updater = Updater(token=os.environ.get('TELEGRAM_BOT_TOKEN'))
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
                     text=("%.1f °C. " % forecast["temperature"] +
                           emojize(forecast["emoji"], use_aliases=True)))


def get_inline(bot, update):
    query = update.inline_query.query
    if not query:
        return
    forecast = weater.get_current_forecast(query)

    results = list()
    results.append(
        InlineQueryResultArticle(
            id="%.1f °C. " % forecast["temperature"] +
            emojize(forecast["emoji"], use_aliases=True),
            title="Weather now",
            input_message_content=InputTextMessageContent("In %s now - %.1f °C. "
                                                          % (query, forecast["temperature"]) +
                                                          emojize(forecast["emoji"], use_aliases=True))
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)


start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

forecast_handler = MessageHandler(Filters.text, get_current_forecast)
dispatcher.add_handler(forecast_handler)

get_inline_handler = InlineQueryHandler(get_inline)
dispatcher.add_handler(get_inline_handler)

updater.start_polling()
