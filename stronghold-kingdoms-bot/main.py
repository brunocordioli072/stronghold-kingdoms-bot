import time
from modules.scounting_module import ScoutingModule
from modules.trading_module import TradingModule
from numpy import random

# Define base interval (in seconds) and randomness range
BASE_INTERVAL = 120  # 2 minutes
VARIATION = 30  # ±30 seconds


def get_random_interval(base, variation):
    return base + random.randint(-variation, variation)


def countdown_sleep(seconds):
    """Sleep with a countdown, printing every second."""
    for remaining in range(seconds, 0, -1):
        print(f"Waiting... {remaining} seconds remaining", end="\r")
        time.sleep(1)
    print(" " * 100, end="\r")  # Clear the line


def run_tasks():
    scouting = ScoutingModule()
    trading = TradingModule()

    while True:
        # Run scouting task
        print("Running scouting task...")
        scouting.run()

        # Run trading task
        print("Running trading task...")
        trading.run()

        # Wait for randomized interval with countdown
        interval = get_random_interval(BASE_INTERVAL, VARIATION)
        print(
            f"Trading completed. Waiting {interval} seconds before scouting.\n")
        countdown_sleep(interval)


if __name__ == "__main__":
    run_tasks()
