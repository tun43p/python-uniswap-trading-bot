import dotenv

from web3 import Web3

from env import Env
from helpers import simulate_job
from jobs import default_job

dotenv.load_dotenv()

web3_client = Web3(Web3.HTTPProvider(Env.rpc_url()))
assert web3_client.is_connected(), "Failed to connect client to RPC"

simulate_job(
    web3_client,
    token_address="0x5FbDB2315678afecb367f032d93F642f64180aa3",
    initial_price=1,
    job=default_job,
    sleep_time=1,
)
