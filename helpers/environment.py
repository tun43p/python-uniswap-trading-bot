import os

from web3 import Web3


def _get_env_variable(name: str) -> str:
    try:
        value = os.environ.get(name)

        if value is None:
            raise ValueError(f"{name} is not set")

        return value
    except Exception as error:
        raise Exception(f"Failed to get {name} variable") from error


def check_env_variables() -> bool:
    """
    Check if all the required environment variables are set
    """

    try:
        get_token_address()
        get_private_key()
        get_rpc_url()
        get_etherscan_api_key()
        get_telegram_api_id()
        get_telegram_api_hash()
        get_telegram_bot_token()
        get_telegram_channel_id()

        return True
    except Exception:
        return False


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

    return Web3().eth.account.from_key(get_private_key()).address


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


def get_telegram_bot_token() -> str:
    """
    Get the Telegram bot token
    """

    return _get_env_variable("TELEGRAM_BOT_TOKEN")


def get_telegram_channel_id() -> str:
    """
    Get the Telegram channel ID
    """

    return _get_env_variable("TELEGRAM_CHANNEL_ID")


def get_docker_client():
    """
    Get the Docker client
    """

    return _get_env_variable("DOCKER_CLIENT")
