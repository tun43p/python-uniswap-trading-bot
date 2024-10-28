from enum import Enum


class TransactionType(Enum):
    """Enum class for transaction types."""

    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    ERROR = "ERROR"
