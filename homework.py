import os
import time
import logging
import requests
import telegram
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(
    'my_logger.log', maxBytes=50000000, backupCount=5)
logger.addHandler(handler)

PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    statuses = {'reviewing': 'работа взята в ревью.',
                'rejected': 'К сожалению в работе нашлись ошибки.',
                'approved': ('Ревьюеру всё понравилось, '
                             'можно приступать к следующему уроку.')}
    stat = statuses.get(homework_status)
    if homework_name is None or homework_status not in statuses:
        return 'ошибка сервера - нет данных о работе или статусе'
    if homework_status == 'reviewing':
        return stat
    return (f'У вас проверили работу "{homework_name}"!\n\n{stat}')


def get_homework_statuses(current_timestamp):
    data = {'from_date': current_timestamp or time.time()}
    headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    try:
        homework_statuses = requests.get(
            'https://praktikum.yandex.ru/api/user_api/homework_statuses/',
            params=data,
            headers=headers,
        )
        return homework_statuses.json()
    except Exception as e:
        logger.exception(f'Бот столкнулся с ошибкой: {e}')


def send_message(message, bot_client):
    logger.info('Отправка сообщения')
    return bot_client.send_message(CHAT_ID, message)


def main():
    logger.debug('Запуск бота')
    # проинициализировать бота здесь
    bot_client = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())  # начальное значение timestamp

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(
                    new_homework.get('homeworks')[0]), bot_client)
            current_timestamp = new_homework.get(
                'current_date', current_timestamp)  # обновить timestamp
            time.sleep(300)  # опрашивать раз в пять минут

        except Exception as e:
            logger.exception(f'Бот столкнулся с ошибкой: {e}')
            send_message(f'Бот столкнулся с ошибкой: {e}', bot_client)
            time.sleep(5)


if __name__ == '__main__':
    main()
