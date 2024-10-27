import dotenv
import time

from helpers import env, log, utils
from jobs.default_job import default_job

dotenv.load_dotenv(dotenv_path=".env")


is_env_variables_set = env.check_env_variables()

if not is_env_variables_set:
    raise Exception("Failed to set environment variables")


def main():
    client = utils.get_client()
    if not client.is_connected():
        raise ConnectionError(
            "Failed to connect to client with RPC_URL={}".format(env.get_rpc_url())
        )

    token_address = env.get_token_address()

    if not client.is_address(token_address):
        raise ValueError(f"Invalid token address: {token_address}")

    initial_price_in_wei = utils.get_token_price_in_wei(client, token_address)

    log.log_info(f"Running default_job for {token_address}")

    # TODO: DELETE THIS !! THIS BUY AT START
    # txn_hash = signals.buy(client, token_address, client.to_wei(0.002, "ether"))
    # current_price_in_eth = client.from_wei(initial_price_in_wei, "ether")
    # price_change_percent = (
    #     (current_price_in_eth - client.from_wei(initial_price_in_wei, "ether"))
    #     / client.from_wei(initial_price_in_wei, "ether")
    # ) * 100
    # log.log_txn(
    #     token_address,
    #     models.TransactionType.BUY,
    #     initial_price_in_wei,
    #     current_price_in_eth,
    #     price_change_percent,
    #     txn_hash,
    # )

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

            log.log_txn(
                token_address,
                transaction_type,
                current_price_in_eth,
                price_change_percent,
                liquidity,
                message,
            )

        except Exception as error:
            log.log_error(error)
            break

    time.sleep(60)


if __name__ == "__main__":
    main()
