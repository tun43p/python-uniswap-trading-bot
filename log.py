import datetime
import logging
import sys

import colorama


_logger = logging.getLogger()
_logger.setLevel(logging.INFO)
_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

_stdout_handler = logging.StreamHandler(sys.stdout)
_stdout_handler.setLevel(logging.DEBUG)
_stdout_handler.setFormatter(_formatter)

_file_handler = logging.FileHandler(
    "logs/{}.log".format(
        int(datetime.datetime.now().timestamp()),
    )
)

_file_handler.setLevel(logging.DEBUG)
_file_handler.setFormatter(_formatter)


_logger.addHandler(_file_handler)
_logger.addHandler(_stdout_handler)


def log_debug(message):
    _logger.debug(message)


def log_info(message):
    _logger.info(message)


def log_warning(message):
    _logger.warning(message)


def log_error(message):
    _logger.error(message)


def log_critical(message, exception: Exception = Exception):
    _logger.critical(message)

    raise exception(message)


def log_info_buy(message):
    _logger.info(f"{colorama.Back.GREEN}BUY{colorama.Style.RESET_ALL} | {message}")


def log_info_sell(message):
    _logger.info(f"{colorama.Back.RED}SELL{colorama.Style.RESET_ALL} | {message}")
