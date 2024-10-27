import dotenv

from helpers import env, utils
from tests import env_test, utils_test

dotenv.load_dotenv(dotenv_path=".env")

print("Env loaded")
print("Connecting to client")

client = utils.get_client()
assert client.is_connected(), "Failed to connect to client with RPC_URL={}".format(
    env.get_rpc_url()
)

print("Connected to client")
print("Running tests")
print("Running env tests")

env_test.run_all_tests()

print("Finished env tests")
print("Running utils tests")

utils_test.run_all_tests(client=client, token_address=env.get_token_address())

print("Finished utils tests")
print("Finished tests")
