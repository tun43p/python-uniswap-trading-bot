from web3 import Web3

from helpers import constants, environment, logger, utils


def buy(
    client: Web3,
    token_address: str,
    amount_in_wei: int,
    slippage_percent: int | float = 0.05,
):
    """
    Buy a token from Uniswap V2
    """

    try:
        public_key = environment.get_public_key()

        if amount_in_wei < 0:
            raise Exception("Invalid amount")

        balance = client.eth.get_balance(public_key)
        if balance < amount_in_wei:
            raise Exception("Insufficient funds")

        liquidity = utils.get_token_liquidity(client, token_address)
        if liquidity < amount_in_wei:
            raise Exception("Insufficient liquidity")

        router = utils.get_router(client)

        eth_to_token_path = [
            client.to_checksum_address(constants.WETH_CONTRACT_ADDRESS),
            client.to_checksum_address(token_address),
        ]

        amount_before_slippage = router.functions.getAmountsOut(
            amount_in_wei,
            eth_to_token_path,
        ).call()[1]

        amount_after_slippage = int(
            amount_before_slippage * (1 - slippage_percent / 100)
        )

        txn_count = client.eth.get_transaction_count(public_key)
        time_limit = client.eth.get_block("latest")["timestamp"] + 60 * 10  # 10 minutes

        txn = router.functions.swapExactETHForTokens(
            amount_after_slippage,
            eth_to_token_path,
            public_key,
            time_limit,
        ).build_transaction(
            {
                "from": public_key,
                "value": amount_in_wei,
                "gas": utils.get_gas_price_for_transaction_in_wei(
                    client, token_address, amount_in_wei
                ),
                "gasPrice": utils.get_gas_price_in_wei(client),
                "nonce": txn_count,
            }
        )

        return _sign(client, txn)
    except Exception as error:
        logger.fatal(f"Buy failed: {error}")


def sell(
    client: Web3,
    token_address: str,
    amount_in_wei: int,
    slippage_percent: int | float = 0.05,
):
    """
    Sell a token on Uniswap V2
    """

    try:
        public_key = environment.get_public_key()

        token_balance = utils.get_token_balance(client, token_address)
        if token_balance < amount_in_wei:
            raise Exception("Insufficient funds")

        liquidity = utils.get_token_liquidity(client, token_address)
        if liquidity < amount_in_wei:
            raise Exception("Insufficient liquidity")

        router = utils.get_router(client)

        token_to_eth_path = [
            client.to_checksum_address(token_address),
            client.to_checksum_address(constants.WETH_CONTRACT_ADDRESS),
        ]

        amount_before_slippage = router.functions.getAmountsOut(
            amount_in_wei,
            token_to_eth_path,
        ).call()[1]

        amount_after_slippage = int(
            amount_before_slippage * (1 - slippage_percent / 100)
        )

        _approve(client, token_address, amount_in_wei)

        txn = router.functions.swapExactTokensForETH(
            amount_before_slippage,
            amount_after_slippage,
            token_to_eth_path,
            public_key,
            client.eth.get_block("latest")["timestamp"] + 60 * 10,  # 10 minutes,
        ).build_transaction(
            {
                "from": public_key,
                "gas": utils.get_gas_price_for_transaction_in_wei(
                    client, token_address, amount_in_wei
                ),
                "gasPrice": utils.get_gas_price_in_wei(client),
                "nonce": client.eth.get_transaction_count(public_key),
            }
        )

        return _sign(client, txn)
    except Exception as error:
        logger.fatal(error)


def _approve(client: Web3, token_address: str, amount_in_wei: int):
    """
    Approve a token for spending by another address (e.g., Uniswap Router)
    """

    try:
        public_key = environment.get_public_key()

        token_contract = client.eth.contract(
            address=token_address,
            abi=utils.get_abi(token_address),
        )

        txn = token_contract.functions.approve(
            client.to_checksum_address(constants.UNISWAP_V2_ROUTER_CONTRACT_ADDRESS),
            amount_in_wei,
        ).build_transaction(
            {
                "from": public_key,
                "gas": utils.get_gas_price_for_transaction_in_wei(
                    client, token_address, amount_in_wei
                ),
                "gasPrice": utils.get_gas_price_in_wei(client),
                "nonce": client.eth.get_transaction_count(public_key),
            }
        )

        return _sign(client, txn, is_approval=True)
    except Exception as error:
        logger.fatal(f"Approval failed: {error}")


def _sign(client: Web3, txn: dict, is_approval: bool = False):
    """
    Sign a transaction
    """

    try:
        signed_txn = client.eth.account.sign_transaction(
            txn, environment.get_private_key()
        )
        txn_hash = client.eth.send_raw_transaction(signed_txn.raw_transaction)

        if client.eth.wait_for_transaction_receipt(txn_hash)["status"] != 1:
            raise Exception(f"{"Approval" if is_approval else "Transaction"} failed")

        return txn_hash
    except Exception as error:
        logger.fatal(f"{'Approval' if is_approval else 'Transaction'} failed: {error}")
