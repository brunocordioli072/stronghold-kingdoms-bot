import json
import os
import sys


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
            "village_1_parish_coords": {
                "x": 1,
                "y": 1
            },
            "parish_trade_button_coords": {
                "x": 1,
                "y": 1
            },
            "sell": {
                "FOODS": {
                    "APPLE": True,
                    "CHEESE": True,
                    "MEAT": True,
                    "BREAD": True,
                    "VEGGIES": True,
                    "FISH": True,
                    "ALE": True
                },
                "LUXURY": {
                    "VENISON": True,
                    "FURNITURE": True,
                    "METALWARE": True,
                    "CLOTHES": True,
                    "WINE": True,
                    "SALT": True,
                    "SPICES": True,
                    "SILK": True
                }
            }
        }

        print("\nNOTICE: A new config.json file has been created with default values.")
        print("Please edit config.json and set the correct values before running the script again.")
        print("Particularly, make sure to set the correct 'device_address' for your BlueStacks instance.")

        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)

        print(f"\nConfiguration saved to {self.CONFIG_FILE}")
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
                print("\nERROR: The config.json file still contains default values!")
                print(
                    "Please edit config.json and set the correct values before running the script.")
                print(
                    "Particularly, make sure to set the correct 'device_address' for your BlueStacks instance.")
                sys.exit(1)

            return config
        except json.JSONDecodeError:
            print(
                f"Error reading {self.CONFIG_FILE}. Creating new configuration.")
            return self.create_config()
