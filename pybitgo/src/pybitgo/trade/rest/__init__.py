from typing import Iterator, List, Optional

from pybitgo.trade.rest.schema import Account, Balance, Order, Trade, User
from requests import Response, Session


class BitGoRESTClient:
    def __init__(self, token: str, base_url: str = "https://app.bitgo.com"):

        self.token = token
        self.base_url = base_url

    def request(self, method: str, url: str, params: dict, json: dict) -> Response:

        with Session() as session:
            session.headers.update({"Authorization": "Bearer " + self.token})
            return session.request(
                method, self.base_url + url, params=params, json=json
            )

    def paginated_request(
        self, method: str, url: str, params: dict, json: dict
    ) -> Iterator[Response]:

        yield (res := self.request(method, url, params, json))

        while "nextBatchPrevId" in res.json():
            params.update({"prevId": res.json()["nextBatchPrevId"]})
            yield (res := self.request(method, url, params, json))

    def get_current_user(self) -> User:
        """Get the current user's public information.

        Returns: GetCurrentUserResponseSchema
        """

        return self.request("GET", "/api/prime/trading/v1/user/current", {}, {}).json()

    def list_accounts(self) -> List[Account]:
        """Get the list of trading accounts that the current user belongs to.

        Returns: List[Account]
        """

        return self.request("GET", "/api/prime/trading/v1/accounts", {}, {}).json()[
            "data"
        ]

    def get_account_balance(self, account_id: str) -> List[Balance]:
        """Get balance information about a single trading account.

        Args:
            account_id (str): The id of the trading account to retrieve.

        Returns: List[Balance]
        """

        return self.request(
            "GET", f"/api/prime/trading/v1/accounts/{account_id}/balances", {}, {}
        ).json()["data"]

    def list_orders(
        self,
        account_id: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        client_order_id: Optional[str] = None,
        date_gte: Optional[str] = None,
        date_lt: Optional[str] = None,
    ) -> Iterator[List[Order]]:
        """Lists all orders from the given trading account.

        Args:
            account_id (str): The id of the trading account to retrieve.
            offset (int): The offset of the first order to return.
            limit (int): The maximum number of orders to return.
            client_order_id (str): The client order id of the order.
            date_gte (str): Return client orders with a creationDate that is greater
                than or equal to the given timestamp
            date_lt (str): Return client orders with a creationDate that is less than
                the given timestamp
        """

        for res in self.paginated_request(
            "GET",
            f"/api/prime/trading/v1/accounts/{account_id}/orders",
            {
                "offset": offset,
                "limit": limit,
                "clientOrderId": client_order_id,
                "dateGte": date_gte,
                "dateLt": date_lt,
            },
            {},
        ):
            yield res.json()["data"]

    def place_market_order(
        self,
        account_id: str,
        product: str,
        side: str,
        quantity: str,
        quantity_currency: str,
        client_order_id: Optional[str] = None,
    ) -> Order:
        """Places a new Market order. Orders can only be placed if your account has a
        sufficient balance. When an order is placed, funds will be reserved for the
        amount of the order.

        Args:
            account_id (str): The id of the trading account to retrieve.
            product (str): Product name e.g. BTC-USD.
            side (str): The side of the order. Either "buy" or "sell".
            quantity (str): The quantity of the order.
            quantity_currency (str): The quantity currency must be in quote currency for
                buy and base currency for sell. e.g. If product is BTC-USD, the base
                currency will be BTC.


        Returns: Order
        """

        assert side in ["buy", "sell"], "side must be either 'buy' or 'sell'"

        return self.request(
            "POST",
            f"/api/prime/trading/v1/accounts/{account_id}/orders",
            {},
            {
                "clientOrderId": client_order_id,
                "product": product,
                "type": "market",
                "side": side,
                "quantity": quantity,
                "quantityCurrency": quantity_currency,
            },
        ).json()

    def place_limit_order(
        self,
        account_id: str,
        product: str,
        side: str,
        quantity: str,
        quantity_currency: str,
        limit_price: str,
        client_order_id: Optional[str] = None,
        duration: Optional[int] = None,
    ) -> Order:
        """Places a new Limit order. Orders can only be placed if your account has a
        sufficient balance. When an order is placed, funds will be reserved for the
        amount of the order.

        Args:
            account_id (str): The id of the trading account to retrieve.
            product (str): Product name e.g. BTC-USD.
            side (str): The side of the order. Either "buy" or "sell".
            quantity (str): The quantity of the order.
            quantity_currency (str): The quantity currency must be in quote currency for
                buy and base currency for sell. e.g. If product is BTC-USD, the base
                currency will be BTC.
            limit_price (str): The limit price of the order.
            client_order_id (str): The client order id of the order.
            duration (int): Duration of the limit order in minutes.

        Returns: Order
        """

        assert side in ["buy", "sell"], "side must be either 'buy' or 'sell'"

        return self.request(
            "POST",
            f"/api/prime/trading/v1/accounts/{account_id}/orders",
            {},
            {
                "clientOrderId": client_order_id,
                "product": product,
                "type": "limit",
                "side": side,
                "quantity": quantity,
                "quantityCurrency": quantity_currency,
                "limitPrice": limit_price,
                "duration": duration,
            },
        ).json()

    def place_twap_order(
        self,
        account_id: str,
        product: str,
        side: str,
        quantity: str,
        quantity_currency: str,
        duration: int,
        interval: int,
        client_order_id: Optional[str] = None,
        limit_price: Optional[str] = None,
        schedule_date: Optional[str] = None,
    ) -> Order:
        """Places a new TWAP order (with or without a limit). Orders can only be placed
        if your account has a sufficient balance. When an order is placed, funds will
        be reserved for the amount of the order.

        Args:
            account_id (str): The id of the trading account to retrieve.
            product (str): Product name e.g. BTC-USD.
            side (str): The side of the order. Either "buy" or "sell".
            quantity (str): The quantity of the order.
            quantity_currency (str): The quantity currency must be in quote currency for
                buy and base currency for sell. e.g. If product is BTC-USD, the base
                currency will be BTC.
            duration (int): Duration of the TWAP order in minutes.
            interval (int): Interval of the TWAP order in minutes.
            client_order_id (str): The client order id of the order.
            limit_price (str): The limit price of the order.
            schedule_date (str): The schedule date of the order.

        Returns: Order
        """

        assert side in ["buy", "sell"], "side must be either 'buy' or 'sell'"

        return self.request(
            "POST",
            f"/api/prime/trading/v1/accounts/{account_id}/orders",
            {},
            {
                "clientOrderId": client_order_id,
                "product": product,
                "type": "twap",
                "side": side,
                "quantity": quantity,
                "quantityCurrency": quantity_currency,
                "duration": duration,
                "interval": interval,
                "limitPrice": limit_price,
                "scheduleDate": schedule_date,
            },
        ).json()

    def get_order(self, account_id: str, order_id: str) -> Order:
        """Get a single order by order id.

        Args:
            account_id (str): The id of the trading account to retrieve.
            order_id (str): The id of the order to retrieve.

        Returns: Order
        """

        return self.request(
            "GET",
            f"/api/prime/trading/v1/accounts/{account_id}/orders/{order_id}",
            {},
            {},
        ).json()

    def cancel_order(self, account_id: str, order_id: str):
        """Attempt to cancel an order that was previously placed. The response will
        return successful if the cancel request is submitted. Use Get Order endpoint or
        subscribe to the orders websocket to get the order details.

        Args:
            account_id (str): The id of the trading account to retrieve.
            order_id (str): The id of the order to retrieve.
        """

        self.request(
            "PUT",
            f"/api/prime/trading/v1/accounts/{account_id}/orders/{order_id}/cancel",
            {},
            {},
        )

    def list_trades(
        self,
        account_id: str,
        offset: Optional[int],
        limit: Optional[int],
        order_id: Optional[str],
        date_gte: Optional[str],
        date_lt: Optional[str],
    ) -> Iterator[List[Trade]]:
        """Lists trades from the trading account. This will include trades that have
        not yet settled.

        Args:
            account_id (str): The id of the trading account to retrieve.
            offset (int): The offset of the first trades to return.
            limit (int): The maximum number of trades to return.
            order_id (str): Return exchange trades with a trade date that is greater
                than or equal to the given timestamp
            date_gte (str): Return exchange trades with a trade date that is less than
                the given timestamp
        """

        for res in self.paginated_request(
            "GET",
            f"/api/prime/trading/v1/accounts/{account_id}/trades",
            {
                "offset": offset,
                "limit": limit,
                "orderId": order_id,
                "dateGte": date_gte,
                "dateLt": date_lt,
            },
            {},
        ):
            yield res.json()
