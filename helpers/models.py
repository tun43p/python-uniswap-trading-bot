from enum import Enum


class TransactionType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    ERROR = "ERROR"
