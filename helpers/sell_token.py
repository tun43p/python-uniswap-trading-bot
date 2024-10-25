from web3 import Web3

from env import Env
from .get_abi_from_etherscan import get_abi_from_etherscan
from .get_token_balance import get_token_balance


def sell_token(
    client: Web3,
    token_address: str,
    amount_in_token: int,
    slippage_percent: int | float = 0.1,
):
    """
    Sell a token on Uniswap V2
    """

    # TODO: Fetch atcual gas price and fees

    public_key = Env.public_key()

    # token_balance = get_token_balance(client, token_address)
    # if token_balance < amount_in_token:
    #     raise Exception("Insufficient funds")

    uniswap_v2_router_contract_address = Env.uniswap_v2_router_contract_address()
    router = client.eth.contract(
        address=uniswap_v2_router_contract_address,
        abi=get_abi_from_etherscan(uniswap_v2_router_contract_address),
    )

    token_to_eth_path = [
        client.to_checksum_address(token_address),
        client.to_checksum_address(
            Env.eth_contract_address()
            # if Env.is_local_network()
            # else Env.weth_contract_address()
        ),
    ]

    # TODO: Fix slippage

    # amount_before_slippage = router.functions.getAmountsOut(
    #     client.to_wei(amount_in_token, "ether"),
    #     token_to_eth_path,
    # ).call()[1]

    amount_before_slippage = client.to_wei(amount_in_token, "ether")
    amount_after_slippage = client.to_wei(
        amount_in_token * (1 - slippage_percent / 100), "ether"
    )

    txn_count = client.eth.get_transaction_count(public_key)
    time_limit = client.eth.get_block("latest")["timestamp"] + 60 * 10  # 10 minutes

    # TODO: Approve token before selling

    txn = router.functions.swapExactTokensForETH(
        amount_before_slippage,
        amount_after_slippage,
        token_to_eth_path,
        public_key,
        time_limit,
    ).build_transaction(
        {
            "from": public_key,
            "gas": 2000000,
            "gasPrice": client.to_wei(50, "gwei"),
            "nonce": txn_count,
        }
    )

    signed_txn = client.eth.account.sign_transaction(txn, Env.private_key())
    txn_hash = client.eth.send_raw_transaction(signed_txn.raw_transaction)

    if client.eth.wait_for_transaction_receipt(txn_hash)["status"] != 1:
        raise Exception("Transaction failed")

    return txn_hash
