import requests

from .get_env_variables import get_etherscan_api_key


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
            "apikey": get_etherscan_api_key(),
        },
    ).json()["result"]
