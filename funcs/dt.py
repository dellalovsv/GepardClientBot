from . import logs
from datetime import datetime as dt
from datetime import timedelta as td


def conv_format(data: str = None) -> str | None:
    try:
        if '-' in data:
            if ':' in data:
                return dt.strptime(data, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M:%S')
            return dt.strptime(data, '%Y-%m-%d').strftime('%d.%m.%Y')
        if '.' in data:
            if ':' in data:
                return dt.strptime(data, '%d.%m.%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            return dt.strptime(data, '%d.%m.%Y').strftime('%Y-%m-%d')
    except Exception as e:
        logs.logger.error(f'funcs.dt.conv_format: {e}')
        return None


def get_now():
    return [
        dt.now().strftime('%Y-%m-%d'),
        dt.now().strftime('%Y-%m-%d %H:%M:%S'),
        dt.now().strftime('%d.%m.%Y'),
        dt.now().strftime('%d.%m.%Y %H:%M:%S'),
    ]


def plus_days(days: int = 0) -> str | None:
    if days <= 0:
        return None
    d = dt.now() + td(days=days)
    return d.strftime('%d.%m.%Y')

