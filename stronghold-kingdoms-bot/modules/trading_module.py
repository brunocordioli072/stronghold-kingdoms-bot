import os
import sys
from services.config_service import ConfigService
from services.template_service import TemplateService
from services.device_service import DeviceService
from services.utils_service import UtilsService


class TradingModule:
    """Manages automated trading operations across multiple villages"""

    def __init__(self):
        self.base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..'))

        self.config_service = ConfigService()
        config = self.config_service.load_config()
        self.device_address = config['device_address']
        self.number_of_villages = config['number_of_villages']
        self.village_1_parish_coords = config['village_1_parish_coords']
        self.sell_config = config["sell"]

        self.template_service = TemplateService(self.base_path)
        self.device_service = DeviceService(
            self.device_address, self.template_service)
        self.utils_service = UtilsService(self.device_service)

        self.template_service.cache_templates()

        self.categories = {
            "foods": [
                {
                    "name": "apple",
                    "price_limit": 500,
                    "coords": {'x': 250, 'y': 215},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 192},
                        "bottom_right": {'x': 176, 'y': 241}
                    }
                },
                {
                    "name": "cheese",
                    "price_limit": 500,
                    "coords": {'x': 221, 'y': 288},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 276},
                        "bottom_right": {'x': 176, 'y': 318}
                    }
                },
                {
                    "name": "meat",
                    "price_limit": 500,
                    "coords": {'x': 246, 'y': 366},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 354},
                        "bottom_right": {'x': 176, 'y': 400}
                    }
                },
                {
                    "name": "bread",
                    "price_limit": 500,
                    "coords": {'x': 205, 'y': 448},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 437},
                        "bottom_right": {'x': 176, 'y': 480}
                    }
                },
                {
                    "name": "veggies",
                    "price_limit": 500,
                    "coords": {'x': 213, 'y': 532},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 516},
                        "bottom_right": {'x': 176, 'y': 559}
                    }
                },
                {
                    "name": "fish",
                    "price_limit": 500,
                    "coords": {'x': 228, 'y': 615},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 595},
                        "bottom_right": {'x': 176, 'y': 641}
                    }
                },
                {
                    "name": "ale",
                    "price_limit": 200,
                    "coords": {'x': 247, 'y': 696},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 675},
                        "bottom_right": {'x': 176, 'y': 719}
                    }
                }

            ],
            "luxury": [
                {
                    "name": "venison",
                    "price_limit": 50,
                    "coords": {'x': 250, 'y': 215},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 192},
                        "bottom_right": {'x': 176, 'y': 241}
                    }
                },
                {
                    "name": "furniture",
                    "price_limit": 50,
                    "coords": {'x': 221, 'y': 288},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 276},
                        "bottom_right": {'x': 176, 'y': 318}
                    }
                },
                {
                    "name": "metalware",
                    "price_limit": 50,
                    "coords": {'x': 246, 'y': 366},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 354},
                        "bottom_right": {'x': 176, 'y': 400}
                    }
                },
                {
                    "name": "clothes",
                    "price_limit": 50,
                    "coords": {'x': 205, 'y': 448},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 437},
                        "bottom_right": {'x': 176, 'y': 480}
                    }
                },
                {
                    "name": "wine",
                    "price_limit": 20,
                    "coords": {'x': 213, 'y': 532},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 516},
                        "bottom_right": {'x': 176, 'y': 559}
                    }
                },
                {
                    "name": "salt",
                    "price_limit": 20,
                    "coords": {'x': 228, 'y': 615},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 595},
                        "bottom_right": {'x': 176, 'y': 641}
                    }
                },
                {
                    "name": "spices",
                    "price_limit": 20,
                    "coords": {'x': 247, 'y': 696},
                    "price_coords": {
                        "top_left": {'x': 78, 'y': 675},
                        "bottom_right": {'x': 176, 'y': 719}
                    }
                },
                {
                    "name": "silk",
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
        """Sells a product by clicking it and confirming the sale"""
        self.device_service.click_coordinates_and_sleep(coords)
        self.device_service.click_coordinates_and_sleep(
            self.buttons["FIND_BEST_SELL_PRICE"])
        self.device_service.click_coordinates_and_sleep(
            self.buttons["SELL_BUTTON"])

    def process_category(self, category_name):
        """Processes all items in a category, selling those above price limit"""
        self.device_service.click_coordinates_and_sleep(
            self.buttons[f"{category_name.upper()}_CATEGORY"])
        for item in self.categories[category_name]:
            if not self.sell_config[category_name][item["name"]]:
                print(f'Configured to not sell {item["name"]}')
                continue

            text = self.device_service.get_numbers_from_coords(
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
        """Handles trading operations for a single village"""
        self.device_service.click_coordinates_and_sleep(
            self.village_1_parish_coords)
        self.device_service.click_coordinates_and_sleep(
            self.buttons["PARISH_TRADE_BUTTON"])
        if not self.has_available_merchants():
            self.device_service.click_coordinates_and_sleep(
                self.buttons["EXIT_BUTTON"])
            return

        for category in ["foods", "luxury"]:
            if not self.process_category(category):
                self.device_service.click_coordinates_and_sleep(
                    self.buttons["EXIT_BUTTON"])
                return

        self.device_service.click_coordinates_and_sleep(
            self.buttons["EXIT_BUTTON"])

    def has_available_merchants(self):
        """Checks if there are merchants available for trading"""
        MERCHANTS_AVAILABLE_TOP_LEFT = {'x': 1324, 'y': 755}
        MERCHANTS_AVAILABLE_BOTTOM_RIGHT = {'x': 1423, 'y': 792}
        text = self.device_service.get_text_from_coords(
            MERCHANTS_AVAILABLE_TOP_LEFT, MERCHANTS_AVAILABLE_BOTTOM_RIGHT)
        return not text.startswith("0/")

    def run(self):
        """Starts the trading process for all villages"""
        try:
            for i in range(self.number_of_villages):
                if i != 0:
                    self.device_service.click_coordinates_and_sleep(
                        self.buttons["NEXT_VILLAGE_BUTTON"], 2)
                self.process_village()

            self.utils_service.go_to_village_1()

        except KeyboardInterrupt:
            print("\nBot stopped by user (Ctrl+C)")
            print("Cleaning up and exiting...")
            sys.exit(0)
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            raise
