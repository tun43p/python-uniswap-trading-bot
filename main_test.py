import dotenv

from helpers import environment, utils
from tests import utils_test

dotenv.load_dotenv(dotenv_path="env/local.env")

print("Env loaded")
print("Connecting to client")

client = utils.get_client()
assert client.is_connected(), "Failed to connect to client with RPC_URL={}".format(
    environment.get_rpc_url()
)

print("Connected to client")
print("Running utils tests")

utils_test.run_all_tests(client=client, token_address=environment.get_token_address())

print("Finished utils tests")
print("Finished tests")
