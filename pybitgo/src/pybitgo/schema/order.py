from typing import Optional, TypedDict


class Order(TypedDict):
    id: str
    accountId: str
    clientOrderId: Optional[str]
    time: str
    creationDate: str
    scheduledDate: Optional[str]
    lastFillDate: Optional[str]
    completionDate: str
    settleDate: Optional[str]
    type: str
    fundingType: str
    status: str
    product: str
    side: str
    quantity: str
    quantityCurrency: str
    filledQuantity: str
    averagePrice: str
