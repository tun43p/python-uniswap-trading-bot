import os
import dotenv

from helpers import env, env_test, utils, utils_test

dotenv.load_dotenv(dotenv_path=".env")

test_token_address = os.environ.get("TEST_TOKEN_ADDRESS")
if test_token_address is None:
    raise ValueError("TEST_TOKEN_ADDRESS is not set")


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

utils_test.run_all_tests(client=client, token_address=test_token_address)

print("Finished utils tests")
print("Finished tests")
