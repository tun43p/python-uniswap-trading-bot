import asyncio
import datetime
import logging

import colorama
from web3 import Web3
import websockets

from helpers import environment, models


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.FileHandler("smart.log"),
        logging.StreamHandler(),
    ],
)


def _format_message(message: str, logging_level: int = logging.INFO) -> str:
    """Format the message with the current timestamp, token address, and logging level.

    :param str message: The message to be formatted.
    :param int logging_level: The logging level.
    :return str: The formatted message.
    """

    from helpers import environment

    return "{}::{}::{}::{}".format(
        datetime.datetime.now().isoformat(),
        environment.get_token_address(),
        logging.getLevelName(logging_level),
        message,
    )


async def _send_ws_message(message: str, logging_level: int = logging.INFO) -> None:
    """Send the message to the WebSocket server.

    :param str message: The message to be sent.
    :param int logging_level: The logging level.
    :return None:
    """

    from helpers import environment

    try:
        if not environment.get_websocket_uri():
            raise ValueError("WEBSOCKET_URI is not set")

        async with websockets.connect(environment.get_websocket_uri()) as websocket:
            await websocket.send(_format_message(message, logging_level))
    except Exception as error:
        logging.error(f"Failed to send message: {error}")


def info(message: str, disable_ws_message: bool = False) -> None:
    """Log an informational message.

    :param str message: The message to be logged.
    :param bool disable_ws_message: If the message should not be sent to the server.
    :return None:
    """

    logging.info(_format_message(message))

    if environment.get_websocket_uri() or disable_ws_message:
        asyncio.run(_send_ws_message(message))


def debug(message: str, disable_ws_message: bool = False) -> None:
    """Log a debug message.

    :param str message: The message to be logged.
    :param bool disable_ws_message: If the message should not be sent to the server.
    :return None:
    """

    logging.debug(_format_message(message, logging.DEBUG))

    if environment.get_websocket_uri() or disable_ws_message:
        asyncio.run(_send_ws_message(message, logging.DEBUG))


def warning(message: str, disable_ws_message: bool = False) -> None:
    """Log a warning message.

    :param str message: The message to be logged.
    :param bool disable_ws_message: If the message should not be sent to the server.
    :return None:
    """

    logging.warning(_format_message(message, logging.WARNING))

    if environment.get_websocket_uri() or disable_ws_message:
        asyncio.run(_send_ws_message(message, logging.WARNING))


def error(message: str, disable_ws_message: bool = False) -> None:
    """Log an error message.

    :param str message: The message to be logged.
    :param bool disable_ws_message: If the message should not be sent to the server.
    :return None:
    """

    logging.error(_format_message(message, logging.ERROR))

    if environment.get_websocket_uri() or disable_ws_message:
        asyncio.run(_send_ws_message(message, logging.ERROR))


def critical(message: str, disable_ws_message: bool = False) -> None:
    """Log a critical message.

    :param str message: The message to be logged.
    :param bool disable_ws_message: If the message should not be sent to the server.
    :return None:
    """

    logging.critical(_format_message(message, logging.CRITICAL))

    if environment.get_websocket_uri() or disable_ws_message:
        asyncio.run(_send_ws_message(message, logging.CRITICAL))


def fatal(message: str, disable_ws_message: bool = False) -> None:
    """Log a fatal message.

    :param str message: The message to be logged.
    :param bool disable_ws_message: If the message should not be sent to the server.
    :return None:
    """

    logging.fatal(_format_message(message, logging.FATAL))

    if environment.get_websocket_uri() or disable_ws_message:
        asyncio.run(_send_ws_message(message, logging.FATAL))

    raise SystemExit(1)


def txn(
    transaction_type: models.TransactionType,
    price_in_wei: int | float,
    price_change_percent: int | float,
    liquidity_in_wei: int | float,
    txn_hash: str | None,
    disable_ws_message: bool = False,
) -> None:
    """Log a transaction message.

    :param models.TransactionType transaction_type: The type of the transaction.
    :param int | float price_in_wei: The price in wei.
    :param int | float price_change_percent: The price change percentage.
    :param int | float liquidity_in_wei: The liquidity in wei.
    :param str | None txn_hash: The transaction hash.
    :param bool disable_ws_message: If the message should not be sent to the server.
    :return None:
    """

    def format_colorized(value, threshold, color_positive, color_negative):
        """Return colorized string based on the threshold."""

        color = color_positive if value >= threshold else color_negative
        return f"{color}{value:.2f}%{colorama.Style.RESET_ALL}"

    price_in_eth = Web3.from_wei(price_in_wei, "ether")
    liquidity_in_eth = Web3.from_wei(liquidity_in_wei, "ether")

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

    info(
        f"{action_color}[{transaction_type.name}]{colorama.Style.RESET_ALL} "
        f"PRICE: {colorama.Fore.CYAN}{price_in_eth} ETH{colorama.Style.RESET_ALL} | "
        f"CHANGE: {price_change_colorized_text} | "
        f"LIQUIDITY: {colorama.Fore.YELLOW}{liquidity_in_eth} ETH{colorama.Style.RESET_ALL}"
        f"{f" | TXN HASH: {colorama.Fore.MAGENTA}{txn_hash}{colorama.Style.RESET_ALL}" if txn_hash else ''}",
        disable_ws_message=disable_ws_message,
    )
