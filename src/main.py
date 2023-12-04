import threading
import asyncio
from library.market.candle import CandleSubscriber


async def start():
    test_key = "trade:1m:fUSD:a30:p2:p30"
    # Create an instance of the CandleSubscriber class
    candle_subscriber = CandleSubscriber(test_key)
    await candle_subscriber.start()


def start_async_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start())
    try:
        loop.run_until_complete(start())
    except Exception as e:
        print(f"Error in WebSocket Daemon: {e}")
    finally:
        loop.close()


def main():
    thread = threading.Thread(target=start_async_loop, daemon=True)
    thread.start()

    while True:
        pass


if __name__ == "__main__":
    main()
