import requests

from web3 import Web3

from helpers import environment, logger


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
        address = environment.get_uniswap_v2_router_contract_address()
        return client.eth.contract(address=address, abi=get_abi(address))
    except Exception as error:
        logger.fatal(f"Failed to get router for contract {address}: {error}")


def get_factory(client: Web3):
    """
    Get the Uniswap V2 Factory contract
    """

    try:
        address = environment.get_uniswap_v2_factory_contract_address()
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
    Get the current price of a token in ETH
    """
    try:
        router = get_router(client)

        path = [
            client.to_checksum_address(environment.get_eth_contract_address()),
            client.to_checksum_address(token_address),
        ]

        return router.functions.getAmountsOut(
            client.to_wei(1, "ether"),
            path,
        ).call()[1]
    except Exception as error:
        logger.fatal(f"Failed to get token price: {error}")


def get_pair_address(client: Web3, token_address: str):
    """
    Get the pair address of a token with ETH
    """

    try:
        factory = get_factory(client)

        return factory.functions.getPair(
            client.to_checksum_address(environment.get_eth_contract_address()),
            client.to_checksum_address(token_address),
        ).call()
    except Exception as error:
        logger.fatal(f"Failed to get pair address: {error}")


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


def get_gas_price_in_wei(client: Web3):
    """
    Get the current gas price
    """

    try:
        # TODO: Check if this is correct or not
        return client.eth.gas_price
    except Exception as error:
        logger.fatal(f"Failed to get gas price: {error}")


def get_gas_price_for_transaction_in_wei(
    client: Web3, token_address: str, amount_in_wei: int
):
    """
    Get the gas estimation for a transaction * 2 for safety
    """

    try:
        estimate_gas = client.eth.estimate_gas(
            {
                "from": client.to_checksum_address(environment.get_public_key()),
                "to": client.to_checksum_address(token_address),
                "value": amount_in_wei,
            }
        )

        # TODO: Check if this is correct or not
        return int(estimate_gas * 2)
    except Exception as error:
        logger.fatal(f"Failed to get gas price for transaction: {error}")
