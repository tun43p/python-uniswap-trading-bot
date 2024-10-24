from web3 import Web3

from helpers import buy_token, get_token_balance, sell_token


def default_job(
    client: Web3,
    token_address: str,
    current_price: int | float,
    initial_price: int | float,
):
    """
    Trading strategy
    - Buy if the price drops by -10%
    - Sell 100% if -20%, 50% if +100%, 10% at +500%, +1000%, +5000%, +10000%, and all
      at +20000%
    """

    token_balance = get_token_balance(client, token_address)

    if current_price < initial_price * 0.9:
        print("Buy if the price drops by -10%")
        return buy_token(client, token_address, 0.10)

    elif current_price <= initial_price * 0.8:
        print("If the price drops by -20%, sell 100%")
        return sell_token(client, token_address, token_balance)

    elif current_price >= initial_price * 2:
        print("If the price increases by 100%, sell 50%")
        return sell_token(client, token_address, token_balance * 0.5)

    for multiplier in [5, 10, 50, 100, 200]:
        if current_price >= initial_price * multiplier:
            print(f"If the price increases by {multiplier}00%, sell 10%")
            return sell_token(client, token_address, token_balance * 0.1)
