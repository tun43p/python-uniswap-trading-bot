import requests

from web3 import Web3, contract

from helpers import constants, environment, logger


def get_client() -> Web3:
    """Get the Web3 client based on the RPC URL.

    :return Web3: The Web3 client.
    """

    try:
        return Web3(Web3.HTTPProvider(environment.get_rpc_url()))
    except Exception as error:
        logger.fatal(f"Failed to get client: {error}")


def get_abi(address: str) -> dict:
    """Get the ABI from Etherscan based on the contract address.

    :param str address: The contract address.
    :return dict: The ABI of the contract.
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


def get_router(client: Web3) -> contract.Contract:
    """Get the Uniswap V2 Router contract.

    :param Web3 client: The Web3 client.
    :return Contract: The Uniswap V2 Router contract.
    """

    try:
        address = constants.UNISWAP_V2_ROUTER_CONTRACT_ADDRESS
        return client.eth.contract(address=address, abi=get_abi(address))
    except Exception as error:
        logger.fatal(f"Failed to get router for contract {address}: {error}")


def get_factory(client: Web3) -> contract.Contract:
    """Get the Uniswap V2 Factory contract.

    :param Web3 client: The Web3 client.
    :return Contract: The Uniswap V2 Factory contract.
    """

    try:
        address = constants.UNISWAP_V2_FACTORY_CONTRACT_ADDRESS
        return client.eth.contract(address=address, abi=get_abi(address))
    except Exception as error:
        logger.fatal(f"Failed to get factory for contract {address}: {error}")


def get_token_price_in_wei(client: Web3, token_address: str) -> int:
    """Get the token price in WEI.

    :param Web3 client: The Web3 client.
    :param str token_address: The token address.
    :return int: The token price in WEI.
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


def get_token_liquidity_in_wei(client: Web3, token_address: str) -> int:
    """Get the token liquidity in WEI.

    :param Web3 client: The Web3 client.
    :param str token_address: The token address.
    :return int: The token liquidity in WEI.
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


def get_token_balance(client: Web3, token_address: str) -> int:
    """Get the token balance of the wallet.

    :param Web3 client: The Web3 client.
    :param str token_address: The token address.
    :return int: The token balance.
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
