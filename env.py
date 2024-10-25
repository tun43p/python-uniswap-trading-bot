import os


def _get_env_variable(name: str) -> str:
    value = os.environ.get(name)

    if value is None:
        raise ValueError(f"{name} is not set")

    return value


class Env:
    @staticmethod
    def public_key() -> str:
        """
        Get the public key of the wallet
        """

        return _get_env_variable("PUBLIC_KEY")

    @staticmethod
    def private_key() -> str:
        """
        Get the private key of the wallet
        """

        return _get_env_variable("PRIVATE_KEY")

    @staticmethod
    def rpc_url() -> str:
        """
        Get the RPC URL
        """

        return _get_env_variable("RPC_URL")

    @staticmethod
    def etherscan_api_key() -> str:
        """
        Get the Etherscan API key
        """

        return _get_env_variable("ETHERSCAN_API_KEY")

    @staticmethod
    def eth_contract_address() -> str:
        """
        Get the ETH contract address
        """

        return _get_env_variable("ETH_CONTRACT_ADDRESS")

    @staticmethod
    def weth_contract_address() -> str:
        """
        Get the WETH contract address
        """

        return _get_env_variable("WETH_CONTRACT_ADDRESS")

    @staticmethod
    def erc20_contract_address() -> str:
        """
        Get the ERC20 contract address
        """

        return _get_env_variable("ERC20_CONTRACT_ADDRESS")

    @staticmethod
    def uniswap_v2_router_contract_address() -> str:
        """
        Get the Uniswap V2 Router contract address
        """
        return _get_env_variable("UNISWAP_V2_ROUTER_CONTRACT_ADDRESS")

    @staticmethod
    def telegram_api_id() -> str:
        """
        Get the Telegram API ID
        """

        return _get_env_variable("TELEGRAM_API_ID")

    @staticmethod
    def telegram_api_hash() -> str:
        """
        Get the Telegram API hash
        """

        return _get_env_variable("TELEGRAM_API_HASH")

    @staticmethod
    def is_local_network() -> bool:
        """
        Check if the network is local
        """

        return "localhost" in _get_env_variable("RPC_URL")
