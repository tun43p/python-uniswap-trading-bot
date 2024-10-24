from web3 import Web3

from .get_abi_from_etherscan import get_abi_from_etherscan
from .get_env_variables import (
    get_erc20_contract_address,
    get_public_key,
    is_local_network,
)


def get_token_balance(client: Web3, token_address: str):
    return (
        client.eth.contract(
            address=token_address,
            abi=get_abi_from_etherscan(
                get_erc20_contract_address() if is_local_network() else token_address
            ),
        )
        .functions.balanceOf(get_public_key())
        .call()
    )
