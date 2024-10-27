import logging
import colorama

from helpers import models

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

_logger = logging.getLogger(__name__)


def log_info(message: str):
    _logger.info(message)


def log_warning(message: str):
    _logger.warning(message)


def log_error(message: str):
    _logger.error(message)


def log_txn(
    token_address: str,
    transaction_type: models.TransactionType,
    price_eth: int | float,
    price_change_percent: int | float,
    liquidity_in_eth: int | float,
    txn_hash: str | None,
):
    def format_colorized(value, threshold, color_positive, color_negative):
        """Return colorized string based on the threshold."""

        color = color_positive if value >= threshold else color_negative
        return f"{color}{value:.2f}%{colorama.Style.RESET_ALL}"

    action_color = colorama.Back.YELLOW
    if transaction_type == models.TransactionType.BUY:
        action_color = colorama.Back.GREEN
    elif (
        transaction_type == models.TransactionType.SELL
        and transaction_type == models.TransactionType.ERROR
    ):
        action_color = colorama.Back.RED

    price_change_colorized_text = format_colorized(
        float(price_change_percent), 0, colorama.Fore.GREEN, colorama.Fore.RED
    )

    _logger.info(
        f"{colorama.Fore.BLUE}{token_address[:6]}...{token_address[-4:]} {action_color}[{transaction_type.name}]{colorama.Style.RESET_ALL} "
        f"PRICE: {colorama.Fore.CYAN}{price_eth:.8f} ETH{colorama.Style.RESET_ALL} | "
        f"CHANGE: {price_change_colorized_text} | "
        f"LIQUIDITY: {colorama.Fore.YELLOW}{liquidity_in_eth}{colorama.Style.RESET_ALL}"
        f"{f" | TXN HASH: {colorama.Fore.MAGENTA}{txn_hash}{colorama.Style.RESET_ALL}" if txn_hash else ''}"
    )
