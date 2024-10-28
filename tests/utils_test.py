from web3 import Web3

from helpers import constants, utils


def _get_abi_test(token_address: str) -> None:
    """Test the get_abi function.

    :param str token_address: The token address.
    :return None:
    """

    print("Test: get_abi")

    assert utils.get_abi(constants.WETH_CONTRACT_ADDRESS) is not None, "ABI is None"

    assert (
        utils.get_abi(constants.UNISWAP_V2_ROUTER_CONTRACT_ADDRESS) is not None
    ), "ABI is None"

    assert (
        utils.get_abi(constants.UNISWAP_V2_FACTORY_CONTRACT_ADDRESS) is not None
    ), "ABI is None"

    assert utils.get_abi(token_address) is not None, "ABI is None"

    print("Test: get_abi passed")


def _get_router_test(client: Web3) -> None:
    """Test the get_router function.

    :param Web3 client: The Web3 client.
    :return None:
    """

    print("Test: get_router")
    assert utils.get_router(client) is not None, "Router is None"
    print("Test: get_router passed")


def _get_factory_test(client: Web3) -> None:
    """Test the get_factory function.

    :param Web3 client: The Web3 client.
    :return None:
    """

    print("Test: get_factory")
    assert utils.get_factory(client) is not None, "Factory is None"
    print("Test: get_factory passed")


def _get_token_price_test(client: Web3, token_address: str) -> None:
    """Test the get_token_price function.

    :param Web3 client: The Web3 client.
    :param str token_address: The token address.
    :return None:
    """

    print("Test: get_token_price")
    token_price_in_wei = utils.get_token_price_in_wei(client, token_address)

    print(
        "Test: get_token_price value:",
        client.from_wei(token_price_in_wei, "ether"),
        "ETH",
    )

    assert token_price_in_wei is not None, "Token price is None"
    print("Test: get_token_price passed")


def _get_token_liquidity_test(client: Web3, token_address: str) -> None:
    """Test the get_token_liquidity function.

    :param Web3 client: The Web3 client.
    :param str token_address: The token address.
    :return None:
    """

    print("Test: get_token_liquidity")
    token_liquidity = utils.get_token_liquidity_in_wei(client, token_address)

    print(
        "Test: get_token_liquidity value:",
        client.from_wei(token_liquidity, "ether"),
        "ETH",
    )

    assert token_liquidity is not None, "Token liquidity is None"
    print("Test: get_token_liquidity passed")


def _get_token_balance_test(client: Web3, token_address: str) -> None:
    """Test the get_token_balance function.

    :param Web3 client: The Web3 client.
    :param str token_address: The token address.
    :return None:
    """

    print("Test: get_token_balance")
    token_balance = utils.get_token_balance(client, token_address)
    print("Test: get_token_balance value:", token_balance)
    assert token_balance is not None, "Token balance is None"
    print("Test: get_token_balance passed")


def run_all_tests(client: Web3, token_address: str) -> None:
    """Run all utils tests.

    :param Web3 client: The Web3 client.
    :param str token_address: The token address.
    :return None:
    """

    _get_abi_test(token_address)
    _get_router_test(client)
    _get_factory_test(client)
    _get_token_price_test(client, token_address)
    _get_token_liquidity_test(client, token_address)
    _get_token_balance_test(client, token_address)
