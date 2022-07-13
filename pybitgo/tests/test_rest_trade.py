import os
from unittest import TestCase

from pybitgo.rest.trade import BitGoRESTClient


class TestRestTrade(TestCase):
    def _get_account_id(self):
        client = BitGoRESTClient(
            os.environ["BITGO_ACCESS_TOKEN"],
            "https://app.bitgo-test.com/api/prime/trading/v1",
        )

        return next(client.list_accounts())["id"]

    def test_get_current_user(self):
        client = BitGoRESTClient(
            os.environ["BITGO_ACCESS_TOKEN"],
            "https://app.bitgo-test.com/api/prime/trading/v1",
        )
        user = client.get_current_user()

        self.assertTrue(
            all(k in user for k in ["id", "firstName", "lastName", "email"])
        )

    def test_list_accounts(self):
        client = BitGoRESTClient(
            os.environ["BITGO_ACCESS_TOKEN"],
            "https://app.bitgo-test.com/api/prime/trading/v1",
        )

        for account in client.list_accounts():
            self.assertTrue(all(k in account for k in ["id", "name"]))

    def test_get_account_balance(self):
        client = BitGoRESTClient(
            os.environ["BITGO_ACCESS_TOKEN"],
            "https://app.bitgo-test.com/api/prime/trading/v1",
        )
        for balance in client.get_account_balance(self._get_account_id()):
            self.assertTrue(
                all(
                    k in balance
                    for k in [
                        "currencyId",
                        "currency",
                        "balance",
                        "heldBalance",
                        "tradableBalance",
                    ]
                )
            )

    def test_list_orders(self):
        client = BitGoRESTClient(
            os.environ["BITGO_ACCESS_TOKEN"],
            "https://app.bitgo-test.com/api/prime/trading/v1",
        )

        for order in client.list_orders(self._get_account_id()):
            self.assertTrue(
                all(
                    k in order
                    for k in [
                        "id",
                        "accountId",
                        "clientOrderId",
                        "time",
                        "creationDate",
                        "scheduledDate",
                        "lastFillDate",
                        "completionDate",
                        "settleDate",
                        "type",
                        "fundingType",
                        "status",
                        "product",
                        "side",
                        "quantity",
                        "quantityCurrency",
                        "filledQuantity",
                        "averagePrice",
                    ]
                )
            )

    def test_place_order(self):
        pass

    def test_get_order(self):
        pass

    def test_cancel_order(self):
        pass

    def test_list_trades(self):
        pass

    def test_get_trade(self):
        pass

    def test_list_currencies(self):
        client = BitGoRESTClient(
            os.environ["BITGO_ACCESS_TOKEN"],
            "https://app.bitgo-test.com/api/prime/trading/v1",
        )

        for currency in client.list_currencies(self._get_account_id()):
            self.assertTrue(all(k in currency for k in ["id", "symbol", "name"]))

    def test_list_products(self):
        client = BitGoRESTClient(
            os.environ["BITGO_ACCESS_TOKEN"],
            "https://app.bitgo-test.com/api/prime/trading/v1",
        )

        for product in client.list_products(self._get_account_id()):
            self.assertTrue(
                all(
                    k in product
                    for k in [
                        "id",
                        "name",
                        "baseCurrencyId",
                        "baseCurrency",
                        "quoteCurrencyId",
                        "quoteCurrency",
                        "baseMinSize",
                        "baseMaxSize",
                        "baseIncrement",
                        "quoteMinSize",
                        "quoteIncrement",
                        "isTradeDisabled",
                    ]
                )
            )

    def test_get_level_one(self):
        client = BitGoRESTClient(
            os.environ["BITGO_ACCESS_TOKEN"],
            "https://app.bitgo-test.com/api/prime/trading/v1",
        )

        level1 = client.get_level1(self._get_account_id(), "TBTC-TUSD*")
        self.assertTrue(
            all(
                k in level1
                for k in [
                    "time",
                    "product",
                    "bidPrice",
                    "bidSize",
                    "askPrice",
                    "askSize",
                ]
            )
        )

    def test_get_level_two(self):
        client = BitGoRESTClient(
            os.environ["BITGO_ACCESS_TOKEN"],
            "https://app.bitgo-test.com/api/prime/trading/v1",
        )

        level2 = client.get_level2(self._get_account_id(), "TBTC-TUSD*")
        self.assertTrue(
            all(
                k in level2
                for k in [
                    "time",
                    "product",
                    "bids",
                    "asks",
                ]
            )
        )
