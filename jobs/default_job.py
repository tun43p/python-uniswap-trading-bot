from enum import Enum
from web3 import Web3

from helpers import buy_token, get_token_balance, sell_token
from models import TransactionType


def default_job(
    client: Web3,
    token_address: str,
    # TODO: Have to pass the current price here ?
    current_price: int | float,
    initial_price: int | float,
    token_balance: int,
) -> tuple[TransactionType, str | None]:
    """
    Default trading strategy
    - Buy if the price drops by -10%
    - Sell 100% if -30%, 50% if +100%, 10% at +500%, +1000%, +5000%, +10000%, and all
      at +20000%
    """

    try:
        if current_price < initial_price * 0.9:
            txn_hash = buy_token(client, token_address, 1)
            return (TransactionType.BUY, txn_hash)

        elif current_price <= initial_price * 0.7:
            txn_hash = sell_token(client, token_address, token_balance)
            return (TransactionType.SELL, txn_hash)

        elif current_price >= initial_price * 2:
            txn_hash = sell_token(client, token_address, token_balance * 0.5)
            return (TransactionType.SELL, txn_hash)

        for multiplier in [5, 10, 50, 100, 200]:
            if current_price >= initial_price * multiplier:
                txn_hash = sell_token(client, token_address, token_balance * 0.1)
                return (TransactionType.SELL, txn_hash)

        return (TransactionType.HOLD, None)
    except Exception as error:
        return (TransactionType.ERROR, error)
