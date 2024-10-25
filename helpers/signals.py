from web3 import Web3

from helpers import env, utils

_public_key = env.get_public_key()
_eth_address = env.get_eth_contract_address()


def buy(
    client: Web3,
    token_address: str,
    amount_in_eth: int | float,
    slippage_percent: int | float = 0.1,
):
    """
    Buy a token from Uniswap V2
    """

    try:
        balance = client.eth.get_balance(_public_key)
        if balance < client.to_wei(amount_in_eth, "ether"):
            raise Exception("Insufficient funds")

        liquidity = utils.get_token_liquidity(client, token_address)
        if liquidity < client.to_wei(amount_in_eth, "ether"):
            raise Exception("Insufficient liquidity")

        router = utils.get_router(client)

        eth_to_token_path = [
            client.to_checksum_address(_eth_address),
            client.to_checksum_address(token_address),
        ]

        amount_before_slippage = router.functions.getAmountsOut(
            client.to_wei(amount_in_eth, "ether"),
            eth_to_token_path,
        ).call()[1]

        amount_after_slippage = client.to_wei(
            amount_in_eth * (1 - slippage_percent / 100), "ether"
        )

        txn_count = client.eth.get_transaction_count(_public_key)
        time_limit = client.eth.get_block("latest")["timestamp"] + 60 * 10  # 10 minutes

        _approve(client, token_address, amount_in_eth)

        txn = router.functions.swapExactETHForTokens(
            amount_before_slippage,
            eth_to_token_path,
            _public_key,
            time_limit,
        ).build_transaction(
            {
                "from": _public_key,
                "value": amount_after_slippage,
                "gas": utils.get_gas_price_for_transaction(
                    client, token_address, amount_in_eth
                ),
                "gasPrice": client.to_wei(utils.get_gas_price(), "gwei"),
                "nonce": txn_count,
            }
        )

        return _sign(client, txn)
    except Exception as error:
        raise Exception("Buy failed") from error


def sell(
    client: Web3,
    token_address: str,
    amount_in_eth: int,
    slippage_percent: int | float = 0.1,
):
    """
    Sell a token on Uniswap V2
    """

    try:
        token_balance = utils.get_token_balance(client, token_address)
        if token_balance < amount_in_eth:
            raise Exception("Insufficient funds")

        liquidity = utils.get_token_liquidity(client, token_address)
        if liquidity < amount_in_eth:
            raise Exception("Insufficient liquidity")

        router = utils.get_router(client)

        token_to_eth_path = [
            client.to_checksum_address(token_address),
            client.to_checksum_address(_eth_address),
        ]

        amount_before_slippage = router.functions.getAmountsOut(
            client.to_wei(amount_in_eth, "ether"),
            token_to_eth_path,
        ).call()[1]

        amount_after_slippage = client.to_wei(
            amount_in_eth * (1 - slippage_percent / 100), "ether"
        )

        _approve(client, token_address, amount_in_eth)

        txn = router.functions.swapExactTokensForETH(
            amount_before_slippage,
            amount_after_slippage,
            token_to_eth_path,
            _public_key,
            client.eth.get_block("latest")["timestamp"] + 60 * 10,  # 10 minutes,
        ).build_transaction(
            {
                "from": _public_key,
                "gas": utils.get_gas_price_for_transaction(
                    client, token_address, amount_in_eth
                ),
                "gasPrice": client.to_wei(utils.get_gas_price(), "gwei"),
                "nonce": client.eth.get_transaction_count(_public_key),
            }
        )

        return _sign(client, txn)
    except Exception as error:
        raise Exception("Sell failed") from error


def _approve(client: Web3, token_address: str, amount_in_eth: int):
    """
    Approve a token for spending by another address (e.g., Uniswap Router)
    """

    try:
        token_contract = client.eth.contract(
            address=token_address,
            abi=utils.get_abi(token_address),
        )

        txn = token_contract.functions.approve(
            client.to_checksum_address(env.get_uniswap_v2_router_contract_address()),
            client.to_wei(amount_in_eth, "ether"),
        ).build_transaction(
            {
                "from": _public_key,
                "gas": utils.get_gas_price_for_transaction(
                    client, token_address, amount_in_eth
                ),
                "gasPrice": client.to_wei(utils.get_gas_price(), "gwei"),
                "nonce": client.eth.get_transaction_count(_public_key),
            }
        )

        return _sign(client, txn, is_approval=True)
    except Exception as error:
        raise Exception("Approval failed") from error


def _sign(client: Web3, txn: dict, is_approval: bool = False):
    """
    Sign a transaction
    """

    try:
        signed_txn = client.eth.account.sign_transaction(txn, env.get_private_key())
        txn_hash = client.eth.send_raw_transaction(signed_txn.raw_transaction)

        if client.eth.wait_for_transaction_receipt(txn_hash)["status"] != 1:
            raise Exception(f"{"Approval" if is_approval else "Transaction"} failed")

        return txn_hash
    except Exception as error:
        raise Exception(
            f"{"Approval" if is_approval else "Transaction"} failed"
        ) from error
