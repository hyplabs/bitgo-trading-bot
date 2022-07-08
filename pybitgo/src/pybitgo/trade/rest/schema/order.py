from typing import TypedDict


class Order(TypedDict):
    id: str
    accountId: str
    clientOrderId: str
    time: str
    creationDate: str
    scheduledDate: str
    lastFillDate: str
    completionDate: str
    settleDate: str
    type: str
    fundingType: str
    status: str
    side: str
    quantity: str
    quantityCurrency: str
    filledQuantity: str
    averagePrice: str
