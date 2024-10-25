from enum import Enum
from web3 import Web3

from helpers import utils, models, signals


def default_job(
    client: Web3,
    token_address: str,
    initial_price: int | float,
) -> tuple[models.TransactionType, str | None]:
    """
    Default trading strategy
    - Buy if the price drops by -10%
    - Sell 100% if -30%, 50% if +100%, 10% at +500%, +1000%, +5000%, +10000%, and all
      at +20000%
    """

    current_price = utils.get_token_price(client, token_address)
    token_balance = utils.get_token_balance(client, token_address)

    try:
        if current_price < initial_price * 0.9:
            txn_hash = signals.buy(client, token_address, 1)
            return (models.TransactionType.BUY, txn_hash)

        # -30% = -20% + -10% from the previous condition
        elif current_price <= initial_price * 0.7:
            txn_hash = signals.sell(client, token_address, token_balance)
            return (models.TransactionType.SELL, txn_hash)

        elif current_price >= initial_price * 2:
            txn_hash = signals.sell(client, token_address, token_balance * 0.5)
            return (models.TransactionType.SELL, txn_hash)

        for multiplier in [5, 10, 50, 100, 200]:
            if current_price >= initial_price * multiplier:
                txn_hash = signals.sell(client, token_address, token_balance * 0.1)
                return (models.TransactionType.SELL, txn_hash)

        return (models.TransactionType.HOLD, None)
    except Exception as error:
        return (models.TransactionType.ERROR, error)
