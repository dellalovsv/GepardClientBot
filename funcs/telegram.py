import config
from funcs import logs

import requests


def sendMessage(tid: int = None, msg: str = None) -> bool:
    """
    Отправляет сообщения пользователя в телеграм
    """
    try:
        data = {
            'chat_id': tid,
            'text': msg,
            'parse_mode': 'HTML'
        }
        if requests.post(config.Telegram.url['sendMessage'], data=data).status_code != 200:
            return False
        return True
    except Exception as e:
        logs.logger.error(f'funcs.telegram.sendMessage: {e}')
        return False
