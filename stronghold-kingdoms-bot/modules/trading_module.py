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
        self.device_id = config['device_id']
        self.number_of_villages = config['number_of_villages']
        self.village_1_parish_coords = config['village_1_parish_coords']

        # Cache templates
        self.template_service.cache_templates()
        self.device_service = DeviceService(
            self.device_id, self.template_service)

        self.categories = {
            "FOODS": [
                {"name": "APPLE", "coords": {'x': 250, 'y': 215}},
                {"name": "CHEESE", "coords": {'x': 221, 'y': 288}},
                {"name": "MEAT", "coords": {'x': 246, 'y': 366}},
                {"name": "BREAD", "coords": {'x': 205, 'y': 448}},
                {"name": "VEGGIES", "coords": {'x': 213, 'y': 532}},
                {"name": "FISH", "coords": {'x': 228, 'y': 615}},
                {"name": "ALE", "coords": {'x': 247, 'y': 696}}
            ],
            "LUXURY": [
                {"name": "VENISON", "coords": {'x': 250, 'y': 215}},
                {"name": "FURNITURE", "coords": {'x': 221, 'y': 288}},
                {"name": "METALWARE", "coords": {'x': 246, 'y': 366}},
                {"name": "CLOTHES", "coords": {'x': 205, 'y': 448}},
                {"name": "WINE", "coords": {'x': 213, 'y': 532}},
                {"name": "SALT", "coords": {'x': 228, 'y': 615}},
                {"name": "SPICES", "coords": {'x': 247, 'y': 696}},
                {"name": "SILK", "coords": {'x': 245, 'y': 768}}
            ]
        }

        self.buttons = {
            "PARISH_TRADE_BUTTON": {'x': 434, 'y': 199},
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
            self.sell_product(item["coords"])
            if not self.has_available_merchants():
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

    def has_available_merchants(self):
        MERCHANTS_AVAILABLE_TOP_LEFT = {'x': 1324, 'y': 755}
        MERCHANTS_AVAILABLE_BOTTOM_RIGHT = {'x': 1423, 'y': 792}
        screen = self.device_service.take_screenshot()
        cropped_image = screen[MERCHANTS_AVAILABLE_TOP_LEFT['y']:MERCHANTS_AVAILABLE_BOTTOM_RIGHT['y'],
                               MERCHANTS_AVAILABLE_TOP_LEFT['x']:MERCHANTS_AVAILABLE_BOTTOM_RIGHT['x']]
        text = pytesseract.image_to_string(cropped_image)
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
