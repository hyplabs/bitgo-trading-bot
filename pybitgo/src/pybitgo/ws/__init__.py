import json
from typing import List

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

    def on_open(self):
        for subscription in self.subscriptions:
            self.send(subscription)

    def on_message(self, msg):
        print(msg)

    def on_error(self, err):
        print(err)

    def on_ping(self, *_):
        """
        The websocket connection is only valid for 60 seconds if no messages are
        sent/recieved. To keep the connection alive, the client must respond to PING
        frames with a PONG.
        """

        self.send("", ABNF.OPCODE_PONG)
