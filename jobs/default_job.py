import time
from web3 import Web3

from log import log_info, log_info_buy, log_info_sell
from helpers import buy_token, get_token_balance, sell_token


def default_job(
    client: Web3,
    token_address: str,
    current_price: int | float,
    initial_price: int | float,
):
    """
    Default trading strategy
    - Buy if the price drops by -10%
    - Sell 100% if -20%, 50% if +100%, 10% at +500%, +1000%, +5000%, +10000%, and all
      at +20000%
    """

    # TODO: While true here

    token_balance = get_token_balance(client, token_address)

    if current_price < initial_price * 0.9:
        log_info_buy("Price dropped by -10%")
        return buy_token(client, token_address, 0.10)

    elif current_price <= initial_price * 0.8:
        log_info_sell("Price dropped by -20%")
        # TODO: Add a stop loss ?
        return sell_token(client, token_address, token_balance)

    elif current_price >= initial_price * 2:
        log_info_sell("Price increased by 100%")
        return sell_token(client, token_address, token_balance * 0.5)

    for multiplier in [5, 10, 50, 100, 200]:
        if current_price >= initial_price * multiplier:
            log_info_sell(f"Price increased by {multiplier}00%")
            return sell_token(client, token_address, token_balance * 0.1)

    log_info("HOLD")

    return None
