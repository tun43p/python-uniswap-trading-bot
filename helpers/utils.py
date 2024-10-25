import requests

from web3 import Web3

from helpers import env

_public_key = env.get_public_key()
_eth_contract_address = env.get_eth_contract_address()


def get_client():
    """
    Get the Web3 client
    """

    return Web3(Web3.HTTPProvider(env.get_rpc_url()))


def get_abi(address: str):
    """
    Get the ABI of a contract from Etherscan
    """

    try:
        return requests.get(
            f"https://api.etherscan.io/api",
            params={
                "module": "contract",
                "action": "getabi",
                "address": address,
                "apikey": env.get_etherscan_api_key(),
            },
        ).json()["result"]
    except Exception as error:
        raise Exception(f"Failed to get ABI for contract {address}") from error


def get_router(client: Web3):
    """
    Get the Uniswap V2 Router contract
    """
    try:
        address = env.get_uniswap_v2_router_contract_address()
        return client.eth.contract(address=address, abi=get_abi(address))
    except Exception as error:
        raise Exception(f"Failed to get router for contract {address}") from error


def get_factory(client: Web3):
    """
    Get the Uniswap V2 Factory contract
    """

    try:
        address = env.get_uniswap_v2_factory_contract_address()
        return client.eth.contract(address=address, abi=get_abi(address))
    except Exception as error:
        raise Exception(f"Failed to get factory for contract {address}") from error


def get_eth_price():
    """
    Get the current price of Ethereum in USD
    """
    try:
        return requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "ethereum", "vs_currencies": "usd"},
        ).json()["ethereum"]["usd"]
    except Exception as error:
        raise Exception("Failed to get ETH price") from error


def get_token_price(client: Web3, token_address: str):
    """
    Get the current price of a token in ETH
    """
    try:
        router = get_router(client)

        path = [
            client.to_checksum_address(_eth_contract_address),
            client.to_checksum_address(token_address),
        ]

        return router.functions.getAmountsOut(1, path).call()[1] / 10**18
    except Exception as error:
        raise Exception("Token is not listed on Uniswap") from error


# TODO: To get_pair ?
def get_pair_address(client: Web3, token_address: str):
    """
    Get the pair address of a token with ETH
    """

    try:
        factory = get_factory(client)

        return factory.functions.getPair(
            client.to_checksum_address(_eth_contract_address),
            client.to_checksum_address(token_address),
        ).call()
    except Exception as error:
        raise Exception("Pair does not exist") from error


def get_token_liquidity(client: Web3, token_address: str):
    """
    Get the liquidity of a token
    """

    try:
        pair_address = get_pair_address(client, token_address)
        pair = client.eth.contract(
            address=pair_address,
            abi=get_abi(pair_address),
        )

        # Why * 2?
        # return pair.functions.getReserves().call()[0] * 2
        return pair.functions.getReserves().call()[0]
    except Exception as error:
        raise Exception("Token is not listed on Uniswap") from error


def get_token_balance(client: Web3, token_address: str):
    """
    Get the token balance of the wallet
    """

    try:
        return (
            client.eth.contract(
                address=token_address,
                abi=get_abi(token_address),
            )
            .functions.balanceOf(_public_key)
            .call()
        )
    except Exception as error:
        raise Exception("Failed to get token balance") from error


def get_gas_price(client: Web3):
    """
    Get the current gas price
    """

    try:
        return client.from_wei(client.eth.gas_price, "gwei")
    except Exception as error:
        raise Exception("Failed to get gas price") from error


def get_gas_price_for_transaction(
    client: Web3, token_address: str, amount_in_eth: int | float
):
    """
    Get the gas estimation for a transaction
    """

    try:
        return client.eth.estimate_gas(
            {
                "from": _public_key,
                "to": token_address,
                "value": client.to_wei(amount_in_eth, "ether"),
            }
        )
    except Exception as error:
        raise Exception("Failed to get gas price for transaction") from error
