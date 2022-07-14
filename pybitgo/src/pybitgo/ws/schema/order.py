from typing import Optional, TypedDict


class Order(TypedDict):
    channel: str
    time: str
    accountId: str
    orderId: str
    clientOrderId: str
    product: str
    status: str
    type: str
    side: str
    quantity: str
    cummulativeQuantity: Optional[str]
    averagePrice: Optional[str]
    traddeId: Optional[str]
    fillQuantity: Optional[str]
    fillPrice: Optional[str]
