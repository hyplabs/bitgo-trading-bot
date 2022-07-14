from abc import abstractmethod
import json
from typing import List
from pybitgo.ws.schema import Level2Error, Level2Snapshot, Order

from websocket import ABNF, WebSocketApp


class BitGoWSClient(WebSocketApp):
    def __init__(
        self, token: str, url: str = "wss://app.bitgo.com/api/prime/trading/v1/ws"
    ):

        super().__init__(
            url,
            header={"Authorization": f"Bearer {token}"},
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_ping=self.on_ping,
        )
        self.subscriptions: List[str] = []

    def subscribe_level2(self, account_id: str, product_id: str) -> "BitGoWSClient":
        """
        The level2 Channel will provide a feed of snapshots of the order book.
        """

        self.subscriptions.append(
            json.dumps(
                {
                    "type": "subscribe",
                    "accountId": account_id,
                    "channel": "level2",
                    "productId": product_id,
                }
            )
        )

        return self

    def subscribe_orders(self, account_id: str) -> "BitGoWSClient":
        """
        The orders channel provides updates to client orders and will let you know if
        an order is: Created, Completed, Canceled, or if there is an Error. This
        channel will also provide updates to individual fills within an order.
        """

        self.subscriptions.append(
            json.dumps(
                {
                    "type": "subscribe",
                    "accountId": account_id,
                    "channel": "orders",
                }
            )
        )

        return self

    def on_open(self, _):
        for subscription in self.subscriptions:
            self.send(subscription)

    def on_message(self, _, msg):
        msg_json = json.loads(msg)

        if msg_json["type"] == "system":
            return

        if msg_json["channel"] == "level2":
            if msg_json["type"] == "snapshot":
                self.on_level2_snapshot(msg_json)

            elif msg_json["type"] == "error":
                self.on_level2_error(msg_json)

        elif msg_json["channel"] == "order":
            self.on_order(msg_json)

    def on_error(self, _, err):
        print(err)

    def on_ping(self, *_):
        """
        The websocket connection is only valid for 60 seconds if no messages are
        sent/recieved. To keep the connection alive, the client must respond to PING
        frames with a PONG.
        """

        self.send("", ABNF.OPCODE_PONG)

    @abstractmethod
    def on_level2_snapshot(self, msg: Level2Snapshot):
        print(msg)

    @abstractmethod
    def on_level2_error(self, msg: Level2Error):
        print(msg)

    @abstractmethod
    def on_order(self, msg: Order):
        print(msg)
