from asyncio import sleep
from web3 import Web3

from helpers import environment


def _get_token_address_test():
    token_address = environment.get_token_address()
    print("token_address", token_address)
    assert Web3.is_address(token_address), "Token address is invalid"


def _get_private_key_test():
    private_key = environment.get_private_key()
    print("private_key", private_key)
    assert len(private_key) == 64, "Private key is not 64 characters long"


def _get_public_key_test():
    public_key = environment.get_public_key()
    print("public_key", public_key)
    assert Web3.is_address(public_key), "Public key is invalid"


def _get_rpc_url_test():
    rpc_url = environment.get_rpc_url()
    print("rpc_url", rpc_url)
    assert rpc_url.startswith("http"), "RPC URL does not start with http"


def _get_etherscan_api_key_test():
    etherscan_api_key = environment.get_etherscan_api_key()
    print("etherscan_api_key", etherscan_api_key)
    assert len(etherscan_api_key) == 34, "Etherscan API key is not 34 characters long"


def _get_eth_contract_address_test():
    eth_address = environment.get_eth_contract_address()
    print("eth_address", eth_address)
    assert Web3.is_address(eth_address), "ETH contract address is invalid"


def _get_uniswap_v2_router_contract_address_test():
    uniswap_v2_router_address = environment.get_uniswap_v2_router_contract_address()
    print("uniswap_v2_router_address", uniswap_v2_router_address)
    assert Web3.is_address(
        uniswap_v2_router_address
    ), "Uniswap V2 Router contract address is invalid"


def _get_uniswap_v2_factory_contract_address_test():
    uniswap_v2_factory_address = environment.get_uniswap_v2_factory_contract_address()
    print("uniswap_v2_factory_address", uniswap_v2_factory_address)
    assert Web3.is_address(
        uniswap_v2_factory_address,
    ), "Uniswap V2 Factory contract address is invalid"


def run_all_tests():
    tests = [
        _get_token_address_test,
        _get_private_key_test,
        _get_public_key_test,
        _get_rpc_url_test,
        _get_etherscan_api_key_test,
        _get_eth_contract_address_test,
        _get_uniswap_v2_router_contract_address_test,
        _get_uniswap_v2_factory_contract_address_test,
    ]

    for test in tests:
        test()
        sleep(5)
