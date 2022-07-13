import json
from typing import List

from websocket import ABNF, WebSocketApp


class BitGoWSlient(WebSocketApp):
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

    def subscribe_level2(self, account_id: str, product_id: str) -> "BitGoWSlient":
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

    def subscribe_order(self, account_id: str) -> "BitGoWSlient":
        self.subscriptions.append(
            json.dumps(
                {
                    "type": "subscribe",
                    "accountId": account_id,
                    "channel": "order",
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

    def on_ping(self, *args):
        self.send("", ABNF.OPCODE_PONG)


if __name__ == "__main__":
    import os

    client = BitGoWSlient(
        os.environ["BITGO_ACCESS_TOKEN"],
        "wss://app.bitgo-test.com/api/prime/trading/v1/ws",
    )

    try:
        client.subscribe_level2("").run_forever()

    except KeyboardInterrupt:
        client.close()
