from datetime import datetime as dt
from datetime import timedelta as td


def get_now():
    return [
        dt.now().strftime('%Y-%m-%d'),
        dt.now().strftime('%Y-%m-%d %H:%M:%S'),
        dt.now().strftime('%d.%m.%Y'),
        dt.now().strftime('%d.%m.%Y %H:%M:%S'),
    ]
