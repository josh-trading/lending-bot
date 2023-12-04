import pytest

from src.library.market.candle import CandleSubscriber


# FIXME
@pytest.mark.asyncio
async def test_initiate_candle_subscriber():
    test_key = "trade:1m:fUSD:a30:p2:30"
    # Create an instance of the CandleSubscriber class
    candle_subscriber = CandleSubscriber(test_key)
    await candle_subscriber.start()
