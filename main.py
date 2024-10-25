import dotenv


from helpers import env, utils

dotenv.load_dotenv(dotenv_path=".env")

client = utils.get_client()
if not client.is_connected():
    raise ConnectionError(
        "Failed to connect to client with RPC_URL={}".format(env.get_rpc_url())
    )
