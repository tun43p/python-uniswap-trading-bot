from web3 import Web3

from .get_abi_from_etherscan import get_abi_from_etherscan
from .get_env_variables import (
    get_private_key,
    get_public_key,
    get_uniswap_v2_router_contract_address,
)


def buy_token(client: Web3, token_address: str, amount_in_eth: int | float):
    """
    Buy a token from Uniswap V2
    """

    public_key = get_public_key()
    uniswap_v2_router_contract_address = get_uniswap_v2_router_contract_address()

    balance = client.eth.get_balance(public_key)
    if balance < client.to_wei(amount_in_eth, "ether"):
        print(balance)
        print(amount_in_eth)
        print(client.to_wei(amount_in_eth, "ether"))
        raise Exception("Insufficient funds")

    eth_to_token_path = [
        # TODO: Find the WETH address
        client.to_checksum_address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"),
        client.to_checksum_address(token_address),
    ]

    txn_count = client.eth.get_transaction_count(public_key)
    time_limit = client.eth.get_block("latest")["timestamp"] + 60 * 10  # 10 minutes

    router = client.eth.contract(
        address=uniswap_v2_router_contract_address,
        abi=get_abi_from_etherscan(uniswap_v2_router_contract_address),
    )

    txn = router.functions.swapExactETHForTokens(
        0,
        eth_to_token_path,
        public_key,
        time_limit,
    ).build_transaction(
        {
            "from": public_key,
            "value": client.to_wei(amount_in_eth, "ether"),
            "gas": 2000000,
            "gasPrice": client.to_wei(50, "gwei"),
            "nonce": txn_count,
        }
    )

    signed_txn = client.eth.account.sign_transaction(txn, get_private_key())
    txn_hash = client.eth.send_raw_transaction(signed_txn.raw_transaction)

    if client.eth.wait_for_transaction_receipt(txn_hash)["status"] != 1:
        raise Exception("Transaction failed")

    return txn_hash
