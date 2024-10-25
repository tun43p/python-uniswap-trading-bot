import requests

from env import Env


def get_abi_from_etherscan(address: str):
    """
    Get the ABI of a contract from Etherscan
    """

    return requests.get(
        f"https://api.etherscan.io/api",
        params={
            "module": "contract",
            "action": "getabi",
            "address": address,
            "apikey": Env.etherscan_api_key(),
        },
    ).json()["result"]
