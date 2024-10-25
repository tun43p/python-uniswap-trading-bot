from web3 import Web3

from helpers import env, utils


def _get_abi_test(token_address: str):
    print("Test: get_abi")

    eth_abi = utils.get_abi(env.get_eth_contract_address())
    print("weth_abi", eth_abi)
    assert eth_abi is not None, "ABI is None"

    router_abi = utils.get_abi(env.get_uniswap_v2_router_contract_address())
    print("router_abi", router_abi)
    assert router_abi is not None, "ABI is None"

    factory_abi = utils.get_abi(env.get_uniswap_v2_factory_contract_address())
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


def _get_eth_price_test():
    eth_price = utils.get_eth_price()
    print("eth_price", eth_price)
    assert eth_price is not None, "ETH price is None"


def _get_token_price_test(client: Web3, token_address: str):
    token_price = utils.get_token_price(client, token_address)
    print("token_price", token_price)
    assert token_price is not None, "Token price is None"


def _get_pair_address_test(client: Web3, token_address: str):
    pair_address = utils.get_pair_address(
        client, token_address if token_address else env.get_weth_contract_address()
    )

    print("pair_address", pair_address)
    assert pair_address is not None, "Pair address is None"


def _get_token_liquidity_test(client: Web3, token_address: str):
    token_liquidity = utils.get_token_liquidity(client, token_address)
    print("token_liquidity", token_liquidity)
    assert token_liquidity is not None, "Token liquidity is None"


def _get_token_balance_test(client: Web3, token_address: str):
    token_balance = utils.get_token_balance(client, token_address)
    print("token_balance", token_balance)
    assert token_balance is not None, "Token balance is None"


def _get_gas_price_test(client: Web3):
    gas_price = utils.get_gas_price(client)
    print("gas_price", gas_price)
    assert gas_price is not None, "Gas price is None"


def _get_gas_price_for_transaction_test(client: Web3, token_address: str):
    gas_price = utils.get_gas_price_for_transaction(client, token_address)
    print("gas_price", gas_price)
    assert gas_price is not None, "Gas price is None"


def run_all_tests(client: Web3, token_address: str):
    _get_abi_test(token_address)
    _get_router_test(client)
    _get_factory_test(client)
    _get_eth_price_test()
    _get_token_price_test(client, token_address)
    _get_pair_address_test(client, token_address)
    _get_token_liquidity_test(client, token_address)
    _get_token_balance_test(client, token_address)
    _get_gas_price_test(client)
    _get_gas_price_for_transaction_test(client, token_address)