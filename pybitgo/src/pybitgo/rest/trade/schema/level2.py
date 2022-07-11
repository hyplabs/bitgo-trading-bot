from typing import List, Tuple, TypedDict


class Level2(TypedDict):
    time: str
    product: str
    bids: List[Tuple[str, str]]
    asks: List[Tuple[str, str]]
