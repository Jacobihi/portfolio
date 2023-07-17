import logging
import os
import sys
from datetime import datetime
from cli.settings import LOG_DIR

today = datetime.now().strftime('%Y_%m_%d')
loggers = {}

LOGGER_BASE_FILE_NAME_ATTR = 'baseFilename'


def get_logger(name):
    # https://stackoverflow.com/questions/7173033/duplicate-log-output-when-using-python-logging-module
    global loggers
    if loggers.get(name):
        return loggers.get(name)
    else:
        log_file = os.path.join(LOG_DIR, '{}_{}'.format(name, today))
        logger = logging.getLogger(name)
        formatter = logging.Formatter(
            '[%(asctime)s] - %(levelname)s: - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
        )

        logger.setLevel(logging.DEBUG)
        # Log ALL to File
        f_handler = logging.FileHandler(filename=log_file, mode='a+')
        f_handler.setLevel(logging.DEBUG)
        f_handler.setFormatter(formatter)
        logger.addHandler(f_handler)

        # Log Less to Console
        c_handler = logging.StreamHandler(sys.stdout)
        c_handler.setLevel(logging.INFO)
        c_handler.setFormatter(formatter)
        logger.addHandler(c_handler)

        loggers[name] = logger

        return logger


def get_file_name_for_logger(logger: logging.Logger) -> str:
    """
    Return the file name for a logger; assumes my style of logger which has 1 file handler.
    Returns the first file name found by any handler.
    """
    for handler in logger.handlers:
        if hasattr(handler, LOGGER_BASE_FILE_NAME_ATTR):
            return getattr(handler, LOGGER_BASE_FILE_NAME_ATTR)


def cleanup_old_logs(directory: str = LOG_DIR, days: int = 14, file_path_suffix: str = ''):
    """
    Logs accumulate locally and we forget about them, so remove any log older than the configured
    days. Default to 14
    :param directory: The directory to perform this removal operation upon
    :param days: The number of days to compare if things are old enough for
    :param file_path_suffix: If '.log' or something indicates your logs; use '' for all files.
    """
    file_names = os.listdir(directory)
    file_names = [
        os.path.join(directory, f)
        for f in file_names
        if file_path_suffix in f and not os.path.isdir(os.path.join(directory, f))
    ]
    old_files = sorted(
        [
            f
            for f in file_names
            if (datetime.now() - datetime.fromtimestamp(os.path.getmtime(f))).days >= days
        ],
        key=lambda f: os.path.getmtime(f),
    )
    if not old_files:
        return None
    ok = input(
        f"Delete {len(old_files)} files older than {days} days (starting {old_files[0]} and ending {old_files[-1]})?"
    )
    if ok.lower() in ['y', 'yes', 'ok', '']:
        for old_file in old_files:
            os.remove(old_file)
