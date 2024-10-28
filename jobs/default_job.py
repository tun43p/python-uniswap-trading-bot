from web3 import Web3

from helpers import utils, models, signals


def default_job(
    client: Web3,
    token_address: str,
    initial_price_in_wei: int,
) -> tuple[models.TransactionType, int, int, str | None]:
    """
    Default trading strategy
    - Buy if the price drops by -10%
    - Sell 100% if -30%, 50% if +100%, 10% at +500%, +1000%, +5000%, +10000%, and all
      at +20000%
    """

    current_price = utils.get_token_price_in_wei(client, token_address)
    token_balance = utils.get_token_balance(client, token_address)

    try:
        if current_price < initial_price_in_wei * 0.9:
            txn_hash = signals.buy(client, token_address, client.to_wei(0.002, "ether"))
            return (models.TransactionType.BUY, current_price, token_balance, txn_hash)

        # -30% = -20% + -10% from the previous condition
        elif current_price <= initial_price_in_wei * 0.7:
            txn_hash = signals.sell(client, token_address, token_balance)
            return (models.TransactionType.SELL, current_price, token_address, txn_hash)

        elif current_price >= initial_price_in_wei * 2:
            txn_hash = signals.sell(client, token_address, token_balance * 0.5)
            return (models.TransactionType.SELL, current_price, token_address, txn_hash)

        for multiplier in [5, 10, 25, 50, 100]:
            if current_price >= initial_price_in_wei * multiplier:
                txn_hash = signals.sell(client, token_address, token_balance * 0.1)
                return (
                    models.TransactionType.SELL,
                    current_price,
                    token_address,
                    txn_hash,
                )

        return (models.TransactionType.HOLD, current_price, token_balance, None)
    except Exception as error:
        return (models.TransactionType.ERROR, current_price, token_address, error)
