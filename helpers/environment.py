import os

from web3 import Web3

from helpers import logger


def _get_env_variable(name: str, not_required: bool = False) -> str:
    """Get the environment variable based on the name and if it is required or not.

    :param str name: The name of the environment variable.
    :param bool not_required: If the environment variable is not required.
    :return str: The value of the environment variable.
    """

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
    """Get the token address.

    :return str: The token address.
    """

    return _get_env_variable("TOKEN_ADDRESS")


def get_private_key() -> str:
    """Get the private key of the wallet.

    :return str: The private key of the wallet.
    """

    return _get_env_variable("WALLET_ADDRESS")


def get_public_key() -> str:
    """Get the public key of the wallet based on the private key.

    :return str: The public key of the wallet.
    """

    try:
        return Web3().eth.account.from_key(get_private_key()).address
    except Exception as error:
        logger.fatal(f"Failed to get PUBLIC_KEY variable: {error}")


def get_rpc_url() -> str:
    """Get the RPC URL.

    :return str: The RPC URL.
    """

    return _get_env_variable("RPC_URL")


def get_etherscan_api_key() -> str:
    """Get the Etherscan API key.

    :return str: The Etherscan API key.
    """

    return _get_env_variable("ETHERSCAN_API_KEY")


def get_websocket_uri() -> str:
    """Get the WebSocket URI.

    :return str: The WebSocket URI.
    """

    return _get_env_variable("WEBSOCKET_URI", not_required=True)
