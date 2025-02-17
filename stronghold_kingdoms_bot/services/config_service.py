import json
import os
import sys
from loguru import logger


class ConfigService:
    def __init__(self):
        self.base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..'))
        self.CONFIG_FILE = os.path.join(self.base_path, "config.json")

    def create_config(self):
        """Create a new configuration file with dummy values"""
        config = {
            "device_address": "127.0.0.1:your-port",
            "number_of_villages": 1,
            "interval_between_loop_in_seconds": 240,
            "village_1_name": "YourVillageName",
            "village_1_parish_coords": {
                "x": 1,
                "y": 1
            },
            "parish_trade_button_coords": {
                "x": 1,
                "y": 1
            },
            "sell": {
                "foods": {
                    "apple": True,
                    "cheese": True,
                    "meat": True,
                    "bread": True,
                    "veggies": True,
                    "fish": True,
                    "ale": True
                },
                "luxury": {
                    "venison": True,
                    "furniture": True,
                    "metalware": True,
                    "clothes": True,
                    "wine": True,
                    "salt": True,
                    "spices": True,
                    "silk": True
                }
            }
        }

        logger.info(
            "\nNOTICE: A new config.json file has been created with default values.")
        logger.info(
            "Please edit config.json and set the correct values before running the script again.")
        logger.info(
            "Particularly, make sure to set the correct 'device_address' for your BlueStacks instance.")

        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)

        logger.info(f"\nConfiguration saved to {self.CONFIG_FILE}")
        return config

    def is_default_config(self, config):
        """Check if the configuration still has dummy values"""
        return config.get('device_address') == '127.0.0.1:your-port'

    def load_config(self):
        """Load configuration from file or create if it doesn't exist"""
        if not os.path.exists(self.CONFIG_FILE):
            self.create_config()
            sys.exit(1)

        try:
            with open(self.CONFIG_FILE, 'r') as f:
                config = json.load(f)

            if self.is_default_config(config):
                logger.info(
                    "\nERROR: The config.json file still contains default values!")
                logger.info(
                    "Please edit config.json and set the correct values before running the script.")
                logger.info(
                    "Particularly, make sure to set the correct 'device_address' for your BlueStacks instance.")
                sys.exit(1)

            return config
        except json.JSONDecodeError:
            logger.info(
                f"Error reading {self.CONFIG_FILE}. Creating new configuration.")
            return self.create_config()
