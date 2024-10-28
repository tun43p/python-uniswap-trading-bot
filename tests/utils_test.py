from web3 import Web3

from helpers import constants, utils


def _get_abi_test(token_address: str):
    print("Test: get_abi")

    eth_abi = utils.get_abi(constants.WETH_CONTRACT_ADDRESS)
    print("eth_abi", eth_abi)
    assert eth_abi is not None, "ABI is None"

    router_abi = utils.get_abi(constants.UNISWAP_V2_ROUTER_CONTRACT_ADDRESS)
    print("router_abi", router_abi)
    assert router_abi is not None, "ABI is None"

    factory_abi = utils.get_abi(constants.UNISWAP_V2_FACTORY_CONTRACT_ADDRESS)
    print("factory_abi", factory_abi)
    assert factory_abi is not None, "ABI is None"

    token_abi = utils.get_abi(token_address)
    print("token_abi", token_abi)
    assert token_abi is not None, "ABI is None"


def _get_router_test(client: Web3):
    router = utils.get_router(client)
    print("router", router)
    assert router is not None, "Router is None"


def _get_factory_test(client: Web3):
    factory = utils.get_factory(client)
    print("factory", factory)
    assert factory is not None, "Factory is None"


def _get_eth_price_in_usd_test():
    eth_price_in_usd = utils.get_eth_price_in_usd()
    print("eth_price", eth_price_in_usd, "$")
    assert eth_price_in_usd is not None, "ETH price is None"


def _get_token_price_test(client: Web3, token_address: str):
    token_price_in_wei = utils.get_token_price_in_wei(client, token_address)
    print("token_price", client.from_wei(token_price_in_wei, "ether"), "ETH")
    assert token_price_in_wei is not None, "Token price is None"


def _get_token_liquidity_test(client: Web3, token_address: str):
    token_liquidity = utils.get_token_liquidity_in_wei(client, token_address)
    print("token_liquidity", client.from_wei(token_liquidity, "ether"), "ETH")
    assert token_liquidity is not None, "Token liquidity is None"


def _get_token_balance_test(client: Web3, token_address: str):
    token_balance = utils.get_token_balance(client, token_address)
    print("token_balance", token_balance)
    assert token_balance is not None, "Token balance is None"


def run_all_tests(client: Web3, token_address: str):
    _get_abi_test(token_address)
    _get_router_test(client)
    _get_factory_test(client)
    _get_eth_price_in_usd_test()
    _get_token_price_test(client, token_address)
    _get_token_liquidity_test(client, token_address)
    _get_token_balance_test(client, token_address)
