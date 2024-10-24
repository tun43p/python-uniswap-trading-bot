import random
import time
import dotenv

from web3 import Web3

from helpers import get_rpc_url
from jobs import default_job

dotenv.load_dotenv()

client = Web3(Web3.HTTPProvider(get_rpc_url()))
assert client.is_connected(), "Failed to connect client to RPC"


# TODO: Delete this or add it to a separate file
def _simulate_trading(token_address: str, initial_price: str):
    current_price = initial_price

    for _ in range(100):
        current_price = current_price * (1 + random.uniform(-0.1, 0.1))

        default_job(
            client,
            token_address,
            current_price,
            initial_price,
        )

        time.sleep(1)


_simulate_trading(
    # TODO: Add a real token address
    token_address="0x5FbDB2315678afecb367f032d93F642f64180aa3",
    initial_price=1,
)
