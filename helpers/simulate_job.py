import random
import time
import colorama
import numpy as np
from web3 import Web3

from log import log_info, log_info_buy, log_info_sell


def simulate_job(
    client: Web3,
    token_address: str,
    initial_price: float,
    job: callable,
    sleep_time: int = 5,
):
    current_price = initial_price
    last_current_price = current_price
    price_changes = []
    i = 0
    token_balance = 0
    volatility = 0

    while i < 100:
        last_current_price = current_price

        if i == 0:
            current_price = initial_price
        if i == 5:
            current_price = last_current_price * 1.1
        elif i == 10:
            current_price = last_current_price * 0.85
        elif i == 12:
            current_price = last_current_price * 2
        else:
            current_price = initial_price * random.uniform(0.8, 1.2)

        percent_change = (
            (current_price - last_current_price) / last_current_price
        ) * 100
        price_changes.append(percent_change)

        if percent_change > 0:
            percent_change_display = (
                f"{colorama.Fore.GREEN}{percent_change:.2f}{colorama.Style.RESET_ALL}%"
            )
        else:
            percent_change_display = (
                f"{colorama.Fore.RED}{percent_change:.2f}{colorama.Style.RESET_ALL}%"
            )

        informations = job(
            client,
            token_address,
            current_price,
            initial_price,
            token_balance,
        )

        if len(price_changes) > 1:
            volatility = np.std(price_changes)

        if "BUY" in informations:
            token_balance += informations[2]
            log_info_buy(
                f"BAL {token_balance} ETH | PRICE {current_price} ETH | VOL {colorama.Fore.CYAN}{volatility:.2f}%{colorama.Style.RESET_ALL} | {percent_change_display}"
            )
        elif "SELL" in informations:
            token_balance = token_balance * informations[2]
            log_info_sell(
                f"BAL {token_balance} ETH | PRICE {current_price} ETH | VOL {colorama.Fore.CYAN}{volatility:.2f}%{colorama.Style.RESET_ALL} | {percent_change_display}"
            )
        else:
            log_info(
                f"{informations[0]} | BAL {token_balance} ETH | PRICE {current_price} ETH | VOL {colorama.Fore.CYAN}{volatility:.2f}%{colorama.Style.RESET_ALL} | {percent_change_display}"
            )

        i += 1

        time.sleep(sleep_time)
