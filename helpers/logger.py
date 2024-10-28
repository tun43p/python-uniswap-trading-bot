import asyncio
import datetime
import logging

import colorama
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
    from helpers import environment

    return "{}::{}::{}::{}".format(
        datetime.datetime.now().isoformat(),
        environment.get_token_address(),
        logging.getLevelName(logging_level),
        message,
    )


async def _send_ws_message(message: str, logging_level: int = logging.INFO) -> None:
    from helpers import environment

    try:
        if not environment.get_websocket_uri():
            raise ValueError("WEBSOCKET_URI is not set")

        async with websockets.connect(environment.get_websocket_uri()) as websocket:
            await websocket.send(_format_message(message, logging_level))
    except Exception as error:
        logging.error(f"Failed to send message: {error}")


def info(message: str, disable_ws_message: bool = False) -> None:
    logging.info(_format_message(message))

    if environment.get_websocket_uri() or disable_ws_message:
        asyncio.run(_send_ws_message(message))


def debug(message: str, disable_ws_message: bool = False) -> None:
    logging.debug(_format_message(message, logging.DEBUG))

    if environment.get_websocket_uri() or disable_ws_message:
        asyncio.run(_send_ws_message(message, logging.DEBUG))


def warning(message: str, disable_ws_message: bool = False) -> None:
    logging.warning(_format_message(message, logging.WARNING))

    if environment.get_websocket_uri() or disable_ws_message:
        asyncio.run(_send_ws_message(message, logging.WARNING))


def error(message: str, disable_ws_message: bool = False) -> None:
    logging.error(_format_message(message, logging.ERROR))

    if environment.get_websocket_uri() or disable_ws_message:
        asyncio.run(_send_ws_message(message, logging.ERROR))


def critical(message: str, disable_ws_message: bool = False) -> None:
    logging.critical(_format_message(message, logging.CRITICAL))

    if environment.get_websocket_uri() or disable_ws_message:
        asyncio.run(_send_ws_message(message, logging.CRITICAL))


def fatal(message: str, disable_ws_message: bool = False) -> None:
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

    info(
        f"{action_color}[{transaction_type.name}]{colorama.Style.RESET_ALL} "
        f"PRICE: {colorama.Fore.CYAN}{price_in_wei} WEI{colorama.Style.RESET_ALL} | "
        f"CHANGE: {price_change_colorized_text} | "
        f"LIQUIDITY: {colorama.Fore.YELLOW}{liquidity_in_wei}{colorama.Style.RESET_ALL} WEI"
        f"{f" | TXN HASH: {colorama.Fore.MAGENTA}{txn_hash}{colorama.Style.RESET_ALL}" if txn_hash else ''}",
        disable_ws_message=disable_ws_message,
    )
