import os


def _get_env_variable(name: str) -> str:
    try:
        value = os.environ.get(name)

        if value is None:
            raise ValueError(f"{name} is not set")

        return value
    except Exception as error:
        raise Exception(f"Failed to get {name} variable") from error


def get_token_address() -> str:
    """
    Get the token address
    """

    return _get_env_variable("TOKEN_ADDRESS")


def get_public_key() -> str:
    """
    Get the public key of the wallet
    """

    return _get_env_variable("PUBLIC_KEY")


def get_private_key() -> str:
    """
    Get the private key of the wallet
    """

    return _get_env_variable("PRIVATE_KEY")


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


def get_eth_contract_address() -> str:
    """
    Get the ETH contract address
    """

    return _get_env_variable("ETH_CONTRACT_ADDRESS")


def get_uniswap_v2_factory_contract_address() -> str:
    """
    Get the Uniswap V2 Factory contract address
    """

    return _get_env_variable("UNISWAP_V2_FACTORY_CONTRACT_ADDRESS")


def get_uniswap_v2_router_contract_address() -> str:
    """
    Get the Uniswap V2 Router contract address
    """
    return _get_env_variable("UNISWAP_V2_ROUTER_CONTRACT_ADDRESS")


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
