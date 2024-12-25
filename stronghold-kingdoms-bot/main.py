import threading
import time
from modules.scounting_module import ScoutingModule
from modules.trading_module import TradingModule

# Lock to ensure no overlapping execution
lock = threading.Lock()

# Time tracking
scouting_last_run = time.time()
trading_last_run = time.time()

# Scouting and trading intervals
SCOUTING_INTERVAL = 120  # 2 minutes
TRADING_INTERVAL = 1800  # 30 minutes


def run_scouting():
    global scouting_last_run
    scounting = ScoutingModule()
    while True:
        with lock:  # Ensure only one task runs at a time
            scounting.run()
            scouting_last_run = time.time()
        time.sleep(SCOUTING_INTERVAL)  # Wait for 2 minutes


def run_trading():
    global trading_last_run
    trading = TradingModule()
    while True:
        with lock:  # Ensure only one task runs at a time
            trading.run()
            trading_last_run = time.time()
        time.sleep(TRADING_INTERVAL)  # Wait for 30 minutes


def display_time_left():
    while True:
        # Check if the lock is acquired
        if not lock.locked():
            scouting_time_left = SCOUTING_INTERVAL - \
                (time.time() - scouting_last_run)
            trading_time_left = TRADING_INTERVAL - \
                (time.time() - trading_last_run)

            print(
                f"Time left for scouting: {max(0, scouting_time_left):.2f} seconds")
            print(
                f"Time left for trading: {max(0, trading_time_left):.2f} seconds")

        time.sleep(1)


if __name__ == "__main__":

    # Start the ScoutingModule in a separate thread
    scouting_thread = threading.Thread(target=run_scouting)
    scouting_thread.daemon = True
    scouting_thread.start()

    # Start the TradingModule in a separate thread
    trading_thread = threading.Thread(target=run_trading)
    trading_thread.daemon = True
    trading_thread.start()

    # Start the time display thread
    display_thread = threading.Thread(target=display_time_left)
    display_thread.daemon = True
    display_thread.start()

    # Keep the main program running
    while True:
        time.sleep(1)
