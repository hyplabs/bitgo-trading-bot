from typing import Iterator, List, Optional
from requests import Response, Session

from pybitgo.trade.rest.schema.user import UserSchema
from pybitgo.trade.rest.schema.account import Account
from pybitgo.trade.rest.schema.balance import Balance
from pybitgo.trade.rest.schema.order import Order


class Request:
    def __init__(self, token: str, base_url: str):

        self.session = Session()
        self.session.headers.update({"Authorization": "Bearer " + token})
        self.base_url = base_url

    def __call__(self, method: str, url: str, params: dict, json: dict) -> Response:

        return self.session.request(
            method, self.base_url + url, params=params, json=json
        )


class PaginatedRequest(Request):
    def __init__(self, token: str, base_url: str):

        super().__init__(token, base_url)

    def __call__(
        self, method: str, url: str, params: dict, json: dict
    ) -> Iterator[Response]:

        yield (res := super().__call__(method, url, params, json))

        while prev_id := res.json()["nextBatchPrevId"]:
            params.update({"prevId": prev_id})
            yield (res := super().__call__(method, url, params, json))


class BitGoRESTClient:
    def __init__(self, token: str, base_url: str = "https://app.bitgo.com"):

        self.token = token
        self.base_url = base_url

    def get_current_user(self) -> UserSchema:
        """Get the current user's public information.

        Returns: GetCurrentUserResponseSchema
        """

        req = Request(self.token, self.base_url)
        return req("GET", "/api/prime/trading/v1/user/current", {}, {}).json()

    def list_accounts(self) -> List[Account]:
        """Get the list of trading accounts that the current user belongs to.

        Returns: List[Account]
        """

        req = Request(self.token, self.base_url)
        return req("GET", "/api/prime/trading/v1/accounts", {}, {}).json()["data"]

    def get_account_balance(self, account_id: str) -> List[Balance]:
        """Get balance information about a single trading account.

        Args:
            account_id (str): The id of the trading account to retrieve.

        Returns: List[Balance]
        """

        req = Request(self.token, self.base_url)
        return req(
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
        """Lists all orders from the given trading account."""

        req = PaginatedRequest(self.token, self.base_url)
        for res in req(
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
        client_order_id: str,
        product: str,
        side: str,
        quantity: str,
        quantityCurrency: str,
    ) -> Order:
        """Places a new Market order. Orders can only be placed if your account has a
        sufficient balance. When an order is placed, funds will be reserved for the
        amount of the order.

        Args:
            account_id (str): The id of the trading account to retrieve.
            client_order_id (str): The clientOrderId of the order.
            product (str): Product name e.g. BTC-USD.
            side (str): The side of the order. Either "buy" or "sell".
            quantity (str): The quantity of the order.
            quantityCurrency (str): The quantity currency must be in quote currency for
                buy and base currency for sell. e.g. If product is BTC-USD, the base
                currency will be BTC.

        Returns: Order
        """

        req = Request(self.token, self.base_url)
        return req(
            "POST",
            f"/api/prime/trading/v1/accounts/{account_id}/orders",
            {},
            {
                "clientOrderId": client_order_id,
                "product": product,
                "type": "market",
                "side": side,
                "quantity": quantity,
                "quantityCurrency": quantityCurrency,
            },
        ).json()["data"]

    def place_limit_order() -> Order:
        pass

    def place_twap_order() -> Order:
        pass
