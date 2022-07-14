from typing import List, Tuple, TypedDict


class Level2Snapshot(TypedDict):
    channel: str
    type: str
    product: str
    time: str
    bids: List[Tuple[str, str]]
    asks: List[Tuple[str, str]]


class Level2Error(TypedDict):
    channel: str
    type: str
    message: str
    time: str
