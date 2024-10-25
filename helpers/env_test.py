from asyncio import sleep
from web3 import Web3

from helpers import env


def _get_public_key_test():
    public_key = env.get_public_key()
    print("public_key", public_key)
    assert Web3.is_address(public_key), "Public key is invalid"


def _get_private_key_test():
    private_key = env.get_private_key()
    print("private_key", private_key)
    assert len(private_key) == 64, "Private key is not 64 characters long"


def _get_rpc_url_test():
    rpc_url = env.get_rpc_url()
    print("rpc_url", rpc_url)
    assert rpc_url.startswith("http"), "RPC URL does not start with http"


def _get_etherscan_api_key_test():
    etherscan_api_key = env.get_etherscan_api_key()
    print("etherscan_api_key", etherscan_api_key)
    assert len(etherscan_api_key) == 34, "Etherscan API key is not 34 characters long"


def _get_eth_contract_address_test():
    eth_address = env.get_eth_contract_address()
    print("eth_address", eth_address)
    assert Web3.is_address(eth_address), "ETH contract address is invalid"


def _get_uniswap_v2_router_contract_address_test():
    uniswap_v2_router_address = env.get_uniswap_v2_router_contract_address()
    print("uniswap_v2_router_address", uniswap_v2_router_address)
    assert Web3.is_address(
        uniswap_v2_router_address
    ), "Uniswap V2 Router contract address is invalid"


def _get_uniswap_v2_factory_contract_address_test():
    uniswap_v2_factory_address = env.get_uniswap_v2_factory_contract_address()
    print("uniswap_v2_factory_address", uniswap_v2_factory_address)
    assert Web3.is_address(
        uniswap_v2_factory_address,
    ), "Uniswap V2 Factory contract address is invalid"


def _get_telegram_api_id_test():
    telegram_api_id = env.get_telegram_api_id()
    print("telegram_api_id", telegram_api_id)
    assert len(telegram_api_id) == 8, "Telegram API ID is not 8 characters long"


def _get_telegram_api_hash_test():
    telegram_api_hash = env.get_telegram_api_hash()
    print("telegram_api_hash", telegram_api_hash)
    assert len(telegram_api_hash) == 32, "Telegram API hash is not 32 characters long"


def run_all_tests():
    tests = [
        _get_public_key_test,
        _get_private_key_test,
        _get_rpc_url_test,
        _get_etherscan_api_key_test,
        _get_eth_contract_address_test,
        _get_uniswap_v2_router_contract_address_test,
        _get_uniswap_v2_factory_contract_address_test,
        _get_telegram_api_id_test,
        _get_telegram_api_hash_test,
    ]

    for test in tests:
        test()
        sleep(5)
