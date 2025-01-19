import time
from stronghold_kingdoms_bot.modules.scouting_module import ScoutingModule
from stronghold_kingdoms_bot.modules.trading_module import TradingModule
from stronghold_kingdoms_bot.services.config_service import ConfigService
from numpy import random
import sys
from loguru import logger

# Define base interval (in seconds) and randomness range
VARIATION = 30  # ±30 seconds

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>"
)

logger.add(
    "app.log",
    rotation="1 day",
    retention="1 day",
    # Clean format for files
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    compression="zip"
)


def get_random_interval(base, variation):
    return base + random.randint(-variation, variation)


def countdown_sleep(seconds):
    """Sleep with a countdown, printing every second."""
    for remaining in range(seconds, 0, -1):
        logger.info(f"Waiting... {remaining:3d} seconds remaining",
                    end="\r", flush=True)
        time.sleep(1)
    logger.info(" " * 40, end="\r", flush=True)


def run_tasks():
    config_service = ConfigService()
    config = config_service.load_config()

    scouting = ScoutingModule()
    trading = TradingModule()

    try:
        while True:
            # Run scouting task
            logger.info("Running scouting task...")
            scouting.run()

            # Run trading task
            logger.info("Running trading task...")
            trading.run()

            # Wait for randomized interval with countdown
            interval = get_random_interval(
                config['interval_between_loop_in_seconds'], VARIATION)
            logger.info(
                f"Trading completed. Waiting {interval} seconds before scouting.\n")
            countdown_sleep(interval)
    except KeyboardInterrupt:
        logger.info("\nBot stopped by user (Ctrl+C)")
        logger.info("Cleaning up and exiting...")
        sys.exit(0)
    except Exception as e:
        logger.info(f"\nAn error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    run_tasks()
