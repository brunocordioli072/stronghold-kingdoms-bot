import time
from modules.scouting_module import ScoutingModule
from modules.trading_module import TradingModule
from services.config_service import ConfigService
from numpy import random
import sys

# Define base interval (in seconds) and randomness range
VARIATION = 30  # ±30 seconds


def get_random_interval(base, variation):
    return base + random.randint(-variation, variation)


def countdown_sleep(seconds):
    """Sleep with a countdown, printing every second."""
    for remaining in range(seconds, 0, -1):
        print(f"Waiting... {remaining:3d} seconds remaining",
              end="\r", flush=True)
        time.sleep(1)
    print(" " * 40, end="\r", flush=True)


def run_tasks():
    config_service = ConfigService()
    config = config_service.load_config()

    scouting = ScoutingModule()
    trading = TradingModule()

    try:
        while True:
            # Run scouting task
            print("Running scouting task...")
            scouting.run()

            # Run trading task
            print("Running trading task...")
            trading.run()

            # Wait for randomized interval with countdown
            interval = get_random_interval(
                config['interval_between_loop_in_seconds'], VARIATION)
            print(
                f"Trading completed. Waiting {interval} seconds before scouting.\n")
            countdown_sleep(interval)
    except KeyboardInterrupt:
        print("\nBot stopped by user (Ctrl+C)")
        print("Cleaning up and exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    run_tasks()
