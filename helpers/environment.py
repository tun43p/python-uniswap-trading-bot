import os

from web3 import Web3

from helpers import logger


def _get_env_variable(name: str, not_required: bool = False) -> str:
    try:
        value = os.environ.get(name)

        if not_required:
            return value
        elif value is None:
            raise ValueError(f"{name} is not set")

        return value
    except Exception as error:
        logger.fatal(f"Failed to get {name} variable: {error}")


def get_token_address() -> str:
    """
    Get the token address
    """

    return _get_env_variable("TOKEN_ADDRESS")


def get_private_key() -> str:
    """
    Get the private key of the wallet
    """

    return _get_env_variable("WALLET_ADDRESS")


def get_public_key() -> str:
    """
    Get the public key of the wallet
    """

    try:
        return Web3().eth.account.from_key(get_private_key()).address
    except Exception as error:
        logger.fatal(f"Failed to get PUBLIC_KEY variable: {error}")


def get_rpc_url() -> str:
    """
    Get the RPC URL
    """

    return _get_env_variable("RPC_URL")


def get_etherscan_api_key() -> str:
    """
    Get the Etherscan API key
    """

    return _get_env_variable("ETHERSCAN_API_KEY")


# TODO: get_weth_contract_address
def get_eth_contract_address() -> str:
    """
    Get the WETH contract address
    """

    return "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"


def get_uniswap_v2_factory_contract_address() -> str:
    """
    Get the Uniswap V2 Factory contract address
    """

    return "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"


def get_uniswap_v2_router_contract_address() -> str:
    """
    Get the Uniswap V2 Router contract address
    """

    return "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"


def get_telegram_api_id() -> str:
    """
    Get the Telegram API ID
    """

    return _get_env_variable("TELEGRAM_API_ID")


def get_telegram_api_hash() -> str:
    """
    Get the Telegram API hash
    """

    return _get_env_variable("TELEGRAM_API_HASH")


def get_telegram_channel_id() -> str:
    """
    Get the Telegram channel ID
    """

    return _get_env_variable("TELEGRAM_CHANNEL_ID")


def get_docker_context():
    """
    Get the Docker context
    """

    docker_context = _get_env_variable("DOCKER_CONTEXT", not_required=True)
    return docker_context if docker_context else "unix://var/run/docker.sock"


def get_websocket_uri():
    """
    Get the WebSocket URI
    """

    return _get_env_variable("WEBSOCKET_URI", not_required=True)
