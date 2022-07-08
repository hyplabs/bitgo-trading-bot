import string
from typing import TypedDict


class Balance(TypedDict):
    currencyId: str
    currency: str
    balance: str
    heldBalance: str
    tradableBalance: str
