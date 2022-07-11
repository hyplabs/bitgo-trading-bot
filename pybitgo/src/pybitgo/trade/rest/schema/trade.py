import string
from typing import TypedDict


class Trade(TypedDict):
    id: str
    orderId: str
    time: str
    product: str
    side: str
    price: str
    quantity: str
    settled: bool
