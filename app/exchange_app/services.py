'''
Telegram-bot
Опрашивает таблицу раз в сутки и следит за сроком поставки.
В случае, если срок прошел, скрипт отправляет уведомление в Telegram
'''

import datetime
import logging
import os

import telegram
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG,
                    format='%(funcName)s, %(asctime)s,'
                           '%(levelname)s, %(name)s, %(message)s')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def send_message(message, bot_client):
    logging.debug('==send message==')
    return bot_client.send_message(CHAT_ID, message)


def main(values):
    bot_client = telegram.Bot(token=TELEGRAM_TOKEN)
    current_date = datetime.date.today()  # текущая дата
    result_list = []
    try:
        for item in values:
            item_date = datetime.datetime.strptime(
                item[3],
                '%d.%m.%Y'
                ).date()
            if item_date < current_date:
                result_list.append(item)
        if len(result_list) > 0:
            send_message(
                f'У данных товаров прошел срок поставки: {result_list}',
                bot_client
                )
    except Exception as exception:
        logging.exception(f'Бот столкнулся с ошибкой: {exception}')
