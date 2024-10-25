from web3 import Web3

from env import Env
from .get_abi_from_etherscan import get_abi_from_etherscan


def get_token_balance(client: Web3, token_address: str):
    # TODO: Fix this

    # router = client.eth.contract(
    #     address=Env.uniswap_v2_router_contract_address(),
    #     abi=get_abi_from_etherscan(Env.uniswap_v2_router_contract_address()),
    # )

    # token_to_eth_path = [
    #     client.to_checksum_address(token_address),
    #     client.to_checksum_address(
    #         Env.eth_contract_address()
    #         if Env.is_local_network()
    #         else Env.weth_contract_address()
    #     ),
    # ]

    # amount_before_slippage = router.functions.getAmountsOut(
    #     1,
    #     token_to_eth_path,
    # ).call()[1]

    return (
        client.eth.contract(
            address=token_address,
            abi=get_abi_from_etherscan(
                Env.erc20_contract_address()
                if Env.is_local_network()
                else token_address
            ),
        )
        .functions.balanceOf(Env.public_key())
        .call()
    )
