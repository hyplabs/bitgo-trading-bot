from typing import Optional, TypedDict


class Product(TypedDict):
    id: str
    name: str
    baseCurrencyId: str
    baseCurrency: str
    quoteCurrencyId: str
    quoteCurrency: str
    baseMinSize: str
    baseMaxSize: Optional[str]
    baseIncrement: Optional[str]
    quoteMinSize: str
    quoteIncrement: str
    isTradeDisabled: bool
