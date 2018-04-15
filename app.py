import time
import os
from datetime import date, timedelta

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from emoji import emojize
import logging
import uuid

from src.weather.weather import Weather

weater = Weather(os.environ.get("DARK_SKY_API_KEY"))
updater = Updater(token=os.environ.get("TELEGRAM_BOT_TOKEN"))
dispatcher = updater.dispatcher

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Hello! It's weather X bot. For to get weather" +
                     "information, enter the name of needed location." +
                     "For example \"Ulan Bator\".")


def send_current_forecast(bot, update):
    forecast = weater.get_current_forecast(update.message.text)
    bot.send_message(chat_id=update.message.chat_id,
                     text=("%.1f °C. " % forecast["temperature"] +
                           emojize(forecast["emoji"], use_aliases=True)))


def send_inline(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()

    results.append(
        InlineQueryResultArticle(
            id=uuid.uuid4(),
            title="Weather now",
            input_message_content=InputTextMessageContent("In %s now  %.1f °C. " %
                                                          (query, weater.get_current_forecast(
                                                              query)["temperature"])
                                                          + emojize(weater.get_current_forecast(query)["emoji"],
                                                                    use_aliases=True)
                                                          )
        )
    )

    results.append(
        InlineQueryResultArticle(
            id=uuid.uuid4(),
            title="Weekly forecast",
            input_message_content=InputTextMessageContent(
                daily_forecast(query)
            )
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)


def daily_forecast(query):
    weekday = date.today()
    weekly_forecast = weater.get_daily_forecast(query)[
        "summary"] + emojize(weater.get_daily_forecast(query)["emoji"], use_aliases=True)
    weekly_forecast += '\n__________________________________________________\n'
    for day in weater.get_daily_forecast(query)["data"]:
        day = dict(day=date.strftime(weekday, '%a'),
                   sum=day.summary,
                   tempMin=day.temperatureMin,
                   tempMax=day.temperatureMax
                   )
        weekly_forecast += '{day}: {sum} Temp range: {tempMin}°C ... {tempMax}°C\n'.format(
            **day)
        weekday += timedelta(days=1)
    return weekly_forecast


start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

forecast_handler = MessageHandler(Filters.text, send_current_forecast)
dispatcher.add_handler(forecast_handler)

send_inline_handler = InlineQueryHandler(send_inline)
dispatcher.add_handler(send_inline_handler)

updater.start_polling()
