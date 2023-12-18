import os
from typing import List, Dict, Any

from bfxapi import Client
from bfxapi.types import Wallet

from library.transaction.funding_offer import FundingOffer


class WalletSubscriber:
    def __init__(self, *args, **kwargs):
        self.client = Client(
            api_key=os.getenv("BFX_API_KEY"),
            api_secret=os.getenv("BFX_API_SECRET"),
            filters=["wallet"],
        )

        if kwargs.get("config"):
            config = kwargs.get("config")
            if "lending_criteria" in config:
                self.lending_criteria = config["lending_criteria"]
                print(f"Lending Criteria: {self.lending_criteria}")
            if "lending_period" in config:
                self.lending_period = config["lending_period"]
                print(f"Lending Period: {self.lending_period}")
            if "offer_type" in config:
                self.offer_type = config["offer_type"]
                print(f"Offer Type: {self.offer_type}")
            if "offer_rate" in config:
                self.offer_rate = config["offer_rate"]
                print(f"Offer Rate: {self.offer_rate}")

        # Register the event handler
        self.client.wss.on("disconnected", self.on_disconnected)
        self.client.wss.on("wallet_snapshot", self.on_wallet_snapshot)
        self.client.wss.on("wallet_update", self.on_wallet_update)

    async def start(self):
        await self.client.wss.start()

    async def close(self):
        await self.client.wss.close()

    def on_disconnected(self, code: int, reason: str):
        if code == 1000 or code == 1001:
            print("Closing the connection without errors!")

    def on_authenticated(self, data: Dict[str, Any]):
        if not data["caps"]["orders"]["read"]:
            raise Exception("This application requires read permissions on orders.")

        if not data["caps"]["positions"]["write"]:
            raise Exception("This application requires write permissions on positions.")

    def on_wallet_snapshot(self, wallets: List[Wallet]):
        for wallet in wallets:
            print(
                f"Wallet: {wallet.wallet_type} | {wallet.currency} | balance: {wallet.balance} | unsettled interest: {wallet.unsettled_interest}"
            )

    def on_wallet_update(self, wallet: Wallet):
        if wallet.wallet_type == "funding":
            print(f"Total balance ({wallet.currency}): {wallet.balance}")
            print(f"Available balance: {wallet.available_balance}")
            if wallet.available_balance > self.lending_criteria:
                print(
                    f"Available balance ({wallet.currency}): {wallet.available_balance} is greater than the lending criteria: {self.lending_criteria}"
                )
                FundingOffer().submit_funding_offer(
                    type=self.offer_type,
                    symbol=f"f{wallet.currency}",
                    amount=str(self.lending_criteria),
                    rate=self.offer_rate,
                    period=self.lending_period,
                )
