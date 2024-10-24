import os
import random
import time
import dotenv
import requests

from web3 import Web3

dotenv.load_dotenv()

DEBUG = True

PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
assert PUBLIC_KEY, "Missing PUBLIC_KEY in environment variables"

PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
assert PRIVATE_KEY, "Missing PRIVATE_KEY in environment variables"

RPC_URL = os.environ.get("RPC_URL")
assert RPC_URL, "Missing RPC_URL in environment variables"

ETHERSCAN_API_KEY = os.environ.get("ETHERSCAN_API_KEY")
assert ETHERSCAN_API_KEY, "Missing ETHERSCAN_API_KEY in environment variables"

ERC20_ADDRESS = os.environ.get("ERC20_ADDRESS")
assert ERC20_ADDRESS, "Missing ERC20_ADDRESS in environment variables"

UNISWAP_V2_ROUTER_ADDRESS = os.environ.get("UNISWAP_V2_ROUTER_ADDRESS")
assert (
    UNISWAP_V2_ROUTER_ADDRESS
), "Missing UNISWAP_V2_ROUTER_ADDRESS in environment variables"


# Connect to the Ethereum network
client = Web3(Web3.HTTPProvider(RPC_URL))
assert client.is_connected(), "Failed to connect client to RPC"


def get_abi_from_etherscan(address):
    """
    Get the ABI of a contract from Etherscan
    """

    return requests.get(
        f"https://api.etherscan.io/api",
        params={
            "module": "contract",
            "action": "getabi",
            "address": address,
            "apikey": ETHERSCAN_API_KEY,
        },
    ).json()["result"]


# Load the Uniswap V2 Router contract
uniswap_router = client.eth.contract(
    address=UNISWAP_V2_ROUTER_ADDRESS,
    abi=get_abi_from_etherscan(UNISWAP_V2_ROUTER_ADDRESS),
)


def buy_token(token_address: str, amount_in_eth: int | float):
    """
    Buy a token from Uniswap V2
    """

    # Check if the wallet has enough funds
    balance = client.eth.get_balance(PUBLIC_KEY)
    if balance < client.to_wei(amount_in_eth, "ether"):
        raise Exception("Insufficient funds")

    # Get the path to swap WETH and the token
    eth_to_token_path = [
        # TODO: Find the WETH address
        client.to_checksum_address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"),
        client.to_checksum_address(token_address),
    ]

    # Get the transaction count and the time limit
    txn_count = client.eth.get_transaction_count(PUBLIC_KEY)
    time_limit = client.eth.get_block("latest")["timestamp"] + 60 * 10  # 10 minutes

    # Build the transaction
    txn = uniswap_router.functions.swapExactETHForTokens(
        0,  # Don't care about the minimum amount of tokens
        eth_to_token_path,
        PUBLIC_KEY,
        time_limit,
    ).buildTransaction(
        {
            "from": PUBLIC_KEY,
            "value": client.to_wei(amount_in_eth, "ether"),
            "gas": 2000000,
            "gasPrice": client.to_wei(50, "gwei"),
            "nonce": txn_count,
        }
    )

    # Sign and send the transaction
    signed_txn = client.eth.account.sign_transaction(txn, PRIVATE_KEY)
    txn_hash = client.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Wait for the transaction to be mined
    if client.eth.wait_for_transaction_receipt(txn_hash)["status"] != 1:
        raise Exception("Transaction failed")

    return txn_hash


def get_token_balance(token_address: str, wallet_public_key: str):
    return (
        client.eth.contract(
            address=token_address, abi=get_abi_from_etherscan(ERC20_ADDRESS)
        )
        .functions.balanceOf(wallet_public_key)
        .call()
    )


def sell_token(token_address: str, amount_in_token: int | float):
    """
    Sell a token on Uniswap V2
    """

    token_balance = get_token_balance(token_address, PUBLIC_KEY)
    if token_balance < amount_in_token:
        raise Exception("Insufficient funds")

    token_to_eth_path = [
        client.to_checksum_address(token_address),
        client.to_checksum_address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"),
    ]

    txn_count = client.eth.get_transaction_count(PUBLIC_KEY)
    time_limit = client.eth.get_block("latest")["timestamp"] + 60 * 10  # 10 minutes

    txn = uniswap_router.functions.swapExactTokensForETH(
        amount_in_token,
        0,
        token_to_eth_path,
        PUBLIC_KEY,
        time_limit,
    ).buildTransaction(
        {
            "from": PUBLIC_KEY,
            "gas": 2000000,
            "gasPrice": client.to_wei(50, "gwei"),
            "nonce": txn_count,
        }
    )

    signed_txn = client.eth.account.sign_transaction(txn, PRIVATE_KEY)
    txn_hash = client.eth.send_raw_transaction(signed_txn.rawTransaction)

    if client.eth.wait_for_transaction_receipt(txn_hash)["status"] != 1:
        raise Exception("Transaction failed")

    return txn_hash


def trading_strategy(
    token_address: str,
    current_price: int | float,
    initial_price: int | float,
):
    """
    Trading strategy
    - Buy if the price drops by -10%
    - Sell 100% if -20%, 50% if +100%, 10% at +500%, +1000%, +5000%, +10000%, and all at +20000%
    """

    token_balance = get_token_balance(token_address, PUBLIC_KEY)

    if current_price < initial_price * 0.9:
        print("Buy if the price drops by -10%")
        return buy_token(token_address, 0.10)

    elif current_price <= initial_price * 0.8:
        print("If the price drops by -20%, sell 100%")
        return sell_token(token_address, token_balance)

    elif current_price >= initial_price * 2:
        print("If the price increases by 100%, sell 50%")
        return sell_token(token_address, token_balance * 0.5)

    for multiplier in [5, 10, 50, 100, 200]:
        if current_price >= initial_price * multiplier:
            print(f"If the price increases by {multiplier}00%, sell 10%")
            return sell_token(token_address, token_balance * 0.1)


def simulate_trading(token_address: str, initial_price: str):
    current_price = initial_price

    for i in range(20):
        change_percent = random.uniform(-0.3, 0.3)
        current_price = current_price * change_percent

        trading_strategy(token_address, current_price, initial_price)

        time.sleep(2)

    pass


simulate_trading(token_address="", initial_price=1)
