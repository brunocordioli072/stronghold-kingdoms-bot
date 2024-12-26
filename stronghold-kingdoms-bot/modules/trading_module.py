import cv2
import numpy as np
from subprocess import run
import time
from datetime import datetime, timedelta
import os
import random
import sys
from services.config_service import ConfigService
from services.template_service import TemplateService
from services.device_service import DeviceService
from typing import Dict
from PIL import Image
import pytesseract


class TradingModule:
    def __init__(self):
        self.base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..'))

        self.config_service = ConfigService()
        self.template_service = TemplateService(self.base_path)

        config = self.config_service.load_config()
        self.device_address = config['device_address']
        self.number_of_villages = config['number_of_villages']
        self.village_1_parish_coords = config['village_1_parish_coords']
        self.sell_config = config["sell"]

        # Cache templates
        self.template_service.cache_templates()
        self.device_service = DeviceService(
            self.device_address, self.template_service)

        self.categories = {
            "FOODS": [
                {
                    "name": "APPLE",
                    "price_limit": 500,
                    "coords": {'x': 250, 'y': 215},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 192},
                        "bottom_right": {'x': 176, 'y': 241}
                    }
                },
                {
                    "name": "CHEESE",
                    "price_limit": 500,
                    "coords": {'x': 221, 'y': 288},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 276},
                        "bottom_right": {'x': 176, 'y': 318}
                    }
                },
                {
                    "name": "MEAT",
                    "price_limit": 500,
                    "coords": {'x': 246, 'y': 366},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 354},
                        "bottom_right": {'x': 176, 'y': 400}
                    }
                },
                {
                    "name": "BREAD",
                    "price_limit": 500,
                    "coords": {'x': 205, 'y': 448},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 437},
                        "bottom_right": {'x': 176, 'y': 480}
                    }
                },
                {
                    "name": "VEGGIES",
                    "price_limit": 500,
                    "coords": {'x': 213, 'y': 532},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 516},
                        "bottom_right": {'x': 176, 'y': 559}
                    }
                },
                {
                    "name": "FISH",
                    "price_limit": 500,
                    "coords": {'x': 228, 'y': 615},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 595},
                        "bottom_right": {'x': 176, 'y': 641}
                    }
                },
                {
                    "name": "ALE",
                    "price_limit": 200,
                    "coords": {'x': 247, 'y': 696},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 675},
                        "bottom_right": {'x': 176, 'y': 719}
                    }
                }

            ],
            "LUXURY": [
                {
                    "name": "VENISON",
                    "price_limit": 50,
                    "coords": {'x': 250, 'y': 215},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 192},
                        "bottom_right": {'x': 176, 'y': 241}
                    }
                },
                {
                    "name": "FURNITURE",
                    "price_limit": 50,
                    "coords": {'x': 221, 'y': 288},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 276},
                        "bottom_right": {'x': 176, 'y': 318}
                    }
                },
                {
                    "name": "METALWARE",
                    "price_limit": 50,
                    "coords": {'x': 246, 'y': 366},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 354},
                        "bottom_right": {'x': 176, 'y': 400}
                    }
                },
                {
                    "name": "CLOTHES",
                    "price_limit": 50,
                    "coords": {'x': 205, 'y': 448},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 437},
                        "bottom_right": {'x': 176, 'y': 480}
                    }
                },
                {
                    "name": "WINE",
                    "price_limit": 20,
                    "coords": {'x': 213, 'y': 532},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 516},
                        "bottom_right": {'x': 176, 'y': 559}
                    }
                },
                {
                    "name": "SALT",
                    "price_limit": 20,
                    "coords": {'x': 228, 'y': 615},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 595},
                        "bottom_right": {'x': 176, 'y': 641}
                    }
                },
                {
                    "name": "SPICES",
                    "price_limit": 20,
                    "coords": {'x': 247, 'y': 696},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 675},
                        "bottom_right": {'x': 176, 'y': 719}
                    }
                },
                {
                    "name": "SILK",
                    "price_limit": 20,
                    "coords": {'x': 245, 'y': 768},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 757},
                        "bottom_right": {'x': 201, 'y': 800}
                    }
                }
            ]
        }

        self.buttons = {
            "PARISH_TRADE_BUTTON": config["parish_trade_button_coords"],
            "FOODS_CATEGORY": {'x': 265, 'y': 41},
            "LUXURY_CATEGORY": {'x': 613, 'y': 40},
            "EXIT_BUTTON": {'x': 1520, 'y': 418},
            "NEXT_VILLAGE_BUTTON": {'x': 970, 'y': 809},
            "FIND_BEST_SELL_PRICE": {'x': 1073, 'y': 662},
            "SELL_BUTTON": {'x': 1323, 'y': 662}
        }

    def sell_product(self, coords):
        self.device_service.click_coordinates_and_sleep(coords)
        self.device_service.click_coordinates_and_sleep(
            self.buttons["FIND_BEST_SELL_PRICE"])
        self.device_service.click_coordinates_and_sleep(
            self.buttons["SELL_BUTTON"])

    def process_category(self, category_name):
        self.device_service.click_coordinates_and_sleep(
            self.buttons[f"{category_name}_CATEGORY"])
        for item in self.categories[category_name]:
            if not self.sell_config[category_name][item["name"]]:
                print(f'Configured to not sell {item["name"]}')
                continue

            text = self.get_numbers_from_coords(
                item['price_coords']['top_left'], item['price_coords']['bottom_right'], item['name'])
            print(f'Found {text.strip()} {item["name"]}')

            if text == "" or text and int(text) < item['price_limit']:
                continue

            self.sell_product(item["coords"])
            if not self.has_available_merchants():
                print("No available merchants")
                return False
        return True

    def process_village(self):
        self.device_service.click_coordinates_and_sleep(
            self.village_1_parish_coords)
        self.device_service.click_coordinates_and_sleep(
            self.buttons["PARISH_TRADE_BUTTON"])
        if not self.has_available_merchants():
            self.device_service.click_coordinates_and_sleep(
                self.buttons["EXIT_BUTTON"])
            return

        for category in ["FOODS", "LUXURY"]:
            if not self.process_category(category):
                self.device_service.click_coordinates_and_sleep(
                    self.buttons["EXIT_BUTTON"])
                return

        self.device_service.click_coordinates_and_sleep(
            self.buttons["EXIT_BUTTON"])

    def get_numbers_from_coords(self, coords1, coords2, name):
        screen = self.device_service.take_screenshot()
        cropped_image = screen[coords1['y']:coords2['y'],
                               coords1['x']:coords2['x']]
        custom_config = r'--psm 6 -c tessedit_char_whitelist=0123456789'

        text = pytesseract.image_to_string(cropped_image, config=custom_config)
        return text

    def get_text_from_coords(self, coords1, coords2):
        screen = self.device_service.take_screenshot()
        cropped_image = screen[coords1['y']:coords2['y'],
                               coords1['x']:coords2['x']]
        text = pytesseract.image_to_string(cropped_image)
        return text

    def has_available_merchants(self):
        MERCHANTS_AVAILABLE_TOP_LEFT = {'x': 1324, 'y': 755}
        MERCHANTS_AVAILABLE_BOTTOM_RIGHT = {'x': 1423, 'y': 792}
        text = self.get_text_from_coords(
            MERCHANTS_AVAILABLE_TOP_LEFT, MERCHANTS_AVAILABLE_BOTTOM_RIGHT)
        return not text.startswith("0/")

    def run(self):
        try:
            for i in range(self.number_of_villages):
                if i != 0:
                    self.device_service.click_coordinates_and_sleep(
                        self.buttons["NEXT_VILLAGE_BUTTON"], 2)
                self.process_village()

            self.device_service.click_coordinates_and_sleep(
                self.buttons["NEXT_VILLAGE_BUTTON"], 2)

        except KeyboardInterrupt:
            print("\nBot stopped by user (Ctrl+C)")
            print("Cleaning up and exiting...")
            sys.exit(0)
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            raise
