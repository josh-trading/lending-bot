import os
import sys
from dotenv import load_dotenv

import threading
import asyncio
from constants import LENDING_CRITERIA, LENDING_PERIOD
from library.market.candle import CandleSubscriber
from library.account.wallet import WalletSubscriber

# Add the path to the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_dir)
load_dotenv()


async def start():
    test_key = "trade:1m:fUSD:a30:p2:p30"
    # Create an instance of the CandleSubscriber class
    # candle_subscriber = CandleSubscriber(test_key)
    # await candle_subscriber.start()
    # Create an instance of the WalletSubscriber class
    wallet_subscriber = WalletSubscriber(
        config={"lending_criteria": LENDING_CRITERIA, "lending_period": LENDING_PERIOD}
    )
    await wallet_subscriber.start()


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
