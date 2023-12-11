import os

from bfxapi import Client
from bfxapi.types import FundingOffer, Notification


class FundingOffer:
    def __init__(self):
        self.client = Client(
            api_key=os.getenv("BFX_API_KEY"), api_secret=os.getenv("BFX_API_SECRET")
        )

    def submit_funding_offer(
        self,
        type,
        symbol,
        amount,
        rate,
        period,
        **kwargs,
    ):
        # Submit a new funding offer
        notification: Notification[
            FundingOffer
        ] = self.client.rest.auth.submit_funding_offer(
            type=type, symbol=symbol, amount=amount, rate=rate, period=period, **kwargs
        )
        print("Funding Offer notification:", notification)
