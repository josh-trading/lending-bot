from bfxapi import Client
from bfxapi.types import Candle
from bfxapi.websocket.subscriptions import Candles, Subscription
from .constants import PUB_WSS_HOST


class CandleSubscriber:
    def __init__(self, key):
        self.client = Client(wss_host=PUB_WSS_HOST)
        self.channel = "candles"
        self.key = key
        self.sub_id = None
        # Register the event handler
        self.client.wss.on("open", self.subscribe)
        self.client.wss.on("disconnected", self.on_disconnected)
        self.client.wss.on("subscribed", self.on_subscribed)
        self.client.wss.on("candles_update", self.on_candles_update)

    async def start(self):
        await self.client.wss.start()

    async def close(self):
        await self.client.wss.close()

    async def subscribe(self):
        await self.client.wss.subscribe(self.channel, self.sub_id, key=self.key)

    async def unsubscribe(self):
        await self.client.wss.unsubscribe(self.sub_id)

    def on_subscribed(self, _sub: Subscription):
        self.sub_id = _sub["sub_id"]
        print(
            "Subscribed to {} with key {}, sub_id: {}.".format(
                _sub["channel"], _sub["key"], self.sub_id
            )
        )

    def on_disconnected(self, code: int, reason: str):
        if code == 1000 or code == 1001:
            print("Closing the connection without errors!")

    def on_candles_update(self, _: Candles, candle: Candle):
        print(f"Candle update for key <{self.key}>: {candle}")
