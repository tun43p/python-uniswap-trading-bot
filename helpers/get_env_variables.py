import os


def _get_env_variable(name: str) -> str:
    value = os.environ.get(name)

    if value is None:
        raise ValueError(f"{name} is not set")

    return value


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


def get_erc20_contract_address() -> str:
    """
    Get the ERC20 contract address
    """

    return _get_env_variable("ERC20_CONTRACT_ADDRESS")


def get_uniswap_v2_router_contract_address() -> str:
    """
    Get the Uniswap V2 Router contract address
    """
    return _get_env_variable("UNISWAP_V2_ROUTER_CONTRACT_ADDRESS")


def is_local_network() -> bool:
    """
    Check if the network is local
    """

    if "localhost" in get_rpc_url():
        return True

    return False
