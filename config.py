from dotenv import load_dotenv

import os


load_dotenv()


class Telegram(object):
    token = os.getenv('TELEGRAM_TOKEN')
    url = {
        'sendMessage': f'https://api.telegram.org/bot{token}/sendMessage'
    }


class DB(object):
    host = os.getenv('DB_HOST')
    port = int(os.getenv('DB_PORT'))
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')
    db = os.getenv('db_name')


class Abills(object):
    secret_key = os.getenv('abills_secret_key')
    attention_days = 3  # при каком остатке, оповещать абонента


class Log(object):
    log_dir = './logs'
