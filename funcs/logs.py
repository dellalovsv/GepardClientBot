import config
from . import dt
from config import Log

import os

from loguru import logger


if Log.log_dir[-1] == '/':
    Log.log_dir[-1].replace('/', '')


if os.path.exists(Log.log_dir) is False:
    os.mkdir(Log.log_dir)


logger.add(
    f'{config.Log.log_dir}/{dt.get_now()[0]}.log',
    format='{time:HH:mm:ss} | {level} | {message}',
    rotation='1 days',
    compression='zip',
    backtrace=True,
    colorize=True
)
