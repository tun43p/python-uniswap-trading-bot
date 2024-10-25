import dotenv


from helpers import env, utils

from jobs.default_job import default_job

dotenv.load_dotenv(dotenv_path=".env")

client = utils.get_client()
if not client.is_connected():
    raise ConnectionError(
        "Failed to connect to client with RPC_URL={}".format(env.get_rpc_url())
    )

tokens = []

while True:
    try:
        for token_address in tokens:
            token_price = utils.get_token_price_in_wei(client, token_address)
            values = default_job(client, token_address, initial_price=token_price)
            print(values)

    except Exception as error:
        print(error)
        break
