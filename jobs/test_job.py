from web3 import Web3

from helpers import utils, models, signals


def test_job(
    client: Web3,
    token_address: str,
    initial_price_in_wei: int,
) -> tuple[models.TransactionType, int, int, str | None]:
    """Test trading strategy.

    - If the price increase by 2%, sell 100%.

    :param Web3 client: The Web3 client.
    :param str token_address: The token address.
    :param int initial_price_in_wei: The initial price in WEI.
    :return tuple[models.TransactionType, int, int, str | None]: The transaction type,
        current price, token balance, and transaction hash.
    """

    current_price = utils.get_token_price_in_wei(client, token_address)
    token_balance = utils.get_token_balance(client, token_address)

    try:
        if current_price >= initial_price_in_wei * 1.02:
            txn_hash = signals.sell(client, token_address, token_balance)
            return (models.TransactionType.SELL, current_price, token_balance, txn_hash)

        return (models.TransactionType.HOLD, current_price, token_balance, None)
    except Exception as error:
        return (models.TransactionType.ERROR, current_price, token_address, error)
