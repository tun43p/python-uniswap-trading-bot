import colorama
import dotenv
import time

dotenv.load_dotenv(dotenv_path=".env.production")

from helpers import env, log, models, utils
from jobs.default_job import default_job


client = utils.get_client()
if not client.is_connected():
    raise ConnectionError(
        "Failed to connect to client with RPC_URL={}".format(env.get_rpc_url())
    )


token_address = env.get_token_address()

if not client.is_address(token_address):
    raise ValueError(f"Invalid token address: {token_address}")

initial_price_in_wei = utils.get_token_price_in_wei(client, token_address)

print(f"Running default_job for {token_address}")

while True:
    try:
        transaction_type, current_price_in_wei, token_balance_in_wei, message = (
            default_job(client, token_address, initial_price_in_wei)
        )

        current_price_in_eth = client.from_wei(current_price_in_wei, "ether")
        price_change_percent = (
            (current_price_in_eth - client.from_wei(initial_price_in_wei, "ether"))
            / client.from_wei(initial_price_in_wei, "ether")
        ) * 100

        liquidity = utils.get_token_liquidity(client, token_address)

        # TODO: Calculate volatility
        # volatility = utils.calculate_volatility(client, token_address)

        log.log_market_info(
            token_address,
            transaction_type,
            current_price_in_eth,
            price_change_percent,
            liquidity,
            message,
        )

    except Exception as error:
        print(error)
        break

time.sleep(60)
