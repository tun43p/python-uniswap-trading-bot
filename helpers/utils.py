import requests

from web3 import Web3

from helpers import constants, environment, logger


def get_client():
    """
    Get the Web3 client
    """

    try:
        return Web3(Web3.HTTPProvider(environment.get_rpc_url()))
    except Exception as error:
        logger.fatal(f"Failed to get client: {error}")


def get_abi(address: str):
    """
    Get the ABI of a contract from Etherscan
    """

    try:
        return requests.get(
            "https://api.etherscan.io/api",
            params={
                "module": "contract",
                "action": "getabi",
                "address": address,
                "apikey": environment.get_etherscan_api_key(),
            },
        ).json()["result"]
    except Exception as error:
        logger.fatal(f"Failed to get ABI for contract {address}: {error}")


def get_router(client: Web3):
    """
    Get the Uniswap V2 Router contract
    """
    try:
        address = constants.UNISWAP_V2_ROUTER_CONTRACT_ADDRESS
        return client.eth.contract(address=address, abi=get_abi(address))
    except Exception as error:
        logger.fatal(f"Failed to get router for contract {address}: {error}")


def get_factory(client: Web3):
    """
    Get the Uniswap V2 Factory contract
    """

    try:
        address = constants.UNISWAP_V2_FACTORY_CONTRACT_ADDRESS
        return client.eth.contract(address=address, abi=get_abi(address))
    except Exception as error:
        logger.fatal(f"Failed to get factory for contract {address}: {error}")


def get_eth_price_in_usd():
    """
    Get the current price of Ethereum in USD
    """
    try:
        return requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "ethereum", "vs_currencies": "usd"},
        ).json()["ethereum"]["usd"]
    except Exception as error:
        logger.fatal(f"Failed to get ETH price: {error}")


def get_token_price_in_wei(client: Web3, token_address: str):
    """
    Get the current price of a token in WEI
    """
    try:
        router = get_router(client)

        path = [
            client.to_checksum_address(token_address),
            client.to_checksum_address(constants.WETH_CONTRACT_ADDRESS),
        ]

        return router.functions.getAmountsOut(
            client.to_wei(1, "ether"),
            path,
        ).call()[-1]
    except Exception as error:
        logger.fatal(f"Failed to get token price: {error}")


def get_token_liquidity_in_wei(client: Web3, token_address: str):
    """
    Get the liquidity of a token in WEI
    """

    try:
        factory = get_factory(client)

        pair_address = factory.functions.getPair(
            client.to_checksum_address(constants.WETH_CONTRACT_ADDRESS),
            client.to_checksum_address(token_address),
        ).call()

        pair = client.eth.contract(
            address=pair_address,
            abi=get_abi(pair_address),
        )

        return pair.functions.getReserves().call()[0]
    except Exception as error:
        logger.fatal(f"Failed to get token liquidity: {error}")


def get_token_balance(client: Web3, token_address: str):
    """
    Get the token balance of the wallet
    """

    try:
        return (
            client.eth.contract(
                address=client.to_checksum_address(token_address),
                abi=get_abi(token_address),
            )
            .functions.balanceOf(
                client.to_checksum_address(environment.get_public_key())
            )
            .call()
        )
    except Exception as error:
        logger.fatal(f"Failed to get token balance: {error}")
