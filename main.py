import cv2
import numpy as np
from subprocess import run
import time
from datetime import datetime, timedelta
import os
import glob
import random
import sys
import json


class StrongholdBot:
    def __init__(self, device_id=None, number_of_villages=None, config_file="config.json", base_path=None):
        self.base_path = base_path or os.path.dirname(
            os.path.abspath(__file__))

        # Configure paths relative to base path
        self.CONFIG_FILE = os.path.join(self.base_path, config_file)
        self.TEMPLATES_DIR = os.path.join(self.base_path, 'templates_bags')

        self.template_cache = {}

        self.GAME_COORDS = {
            'NEXT_VILLAGE': {'x': 970, 'y': 809},
            'HOME_BUTTON': {'x': 1554, 'y': 762},
            'MIDDLE_OF_SCREEN': {'x': 794, 'y': 439},
        }

        if device_id and number_of_villages:
            self.device_id = device_id
            self.number_of_villages = number_of_villages
        else:
            config = self.load_config()
            self.device_id = config['device_id']
            self.number_of_villages = config['number_of_villages']

        # Cache templates
        self.cache_templates()

        # Connect to the device
        self.connect_device()

    def cache_templates(self):
        """Cache all template images into memory."""
        template_paths = self.get_template_paths()
        for path in template_paths:
            self.template_cache[path] = cv2.imread(path)

        SCOUT_BUTTON_PATH = os.path.join(
            self.base_path, 'templates_general', 'scout_button.png')
        GO_BUTTON_PATH = os.path.join(
            self.base_path, 'templates_general', 'go_button.png')
        SCOUT_EXIT_BUTTON_PATH = os.path.join(
            self.base_path, 'templates_general', 'scout_exit_button.png')

        # Add specific templates to the cache
        self.template_cache['SCOUT_BUTTON'] = cv2.imread(
            SCOUT_BUTTON_PATH)
        self.template_cache['GO_BUTTON'] = cv2.imread(GO_BUTTON_PATH)
        self.template_cache['SCOUT_EXIT_BUTTON'] = cv2.imread(
            SCOUT_EXIT_BUTTON_PATH)

    def connect_device(self):
        """Connect to the specified device using ADB"""
        run(['adb', 'connect', self.device_id])

    def create_config(self):
        """Create a new configuration file with dummy values"""
        config = {
            "device_id": "127.0.0.1:your-port",
            "number_of_villages": 1
        }

        print("\nNOTICE: A new config.json file has been created with default values.")
        print("Please edit config.json and set the correct values before running the script again.")
        print("Particularly, make sure to set the correct 'device_id' for your BlueStacks instance.")

        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)

        print(f"\nConfiguration saved to {self.CONFIG_FILE}")
        return config

    def is_default_config(self, config):
        """Check if the configuration still has dummy values"""
        return config.get('device_id') == '127.0.0.1:your-port'

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
                    "Particularly, make sure to set the correct 'device_id' for your BlueStacks instance.")
                sys.exit(1)

            return config
        except json.JSONDecodeError:
            print(
                f"Error reading {self.CONFIG_FILE}. Creating new configuration.")
            return self.create_config()

    def add_random_offset(self, x, y, max_radius=5):
        """Add a random offset to coordinates within a specified radius"""
        offset_x = int(np.random.normal(0, max_radius/3))
        offset_y = int(np.random.normal(0, max_radius/3))

        offset_x = max(min(offset_x, max_radius), -max_radius)
        offset_y = max(min(offset_y, max_radius), -max_radius)

        return x + offset_x, y + offset_y

    def adb_command(self, command):
        """Run ADB command for the device"""
        return run(['adb', '-s', self.device_id] + command, capture_output=True)

    def take_screenshot(self):
        """Take and return a screenshot from the device"""
        self.adb_command(['shell', 'screencap', '-p', '/sdcard/screen.png'])
        self.adb_command(['pull', '/sdcard/screen.png', '.'])
        return cv2.imread('screen.png')

    def find(self, template_path, threshold=0.7):
        """Find and click on a template image"""
        template = self.template_cache.get(template_path)
        if template is None:
            print(f"Template not found in cache: {template_path}")
            return False

        screen = self.take_screenshot()

        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            print(f"Found {template_path}, max_val: {max_val}")
            return True
        print(f"Didn't find {template_path}, max_val: {max_val}")
        return False

    def find_and_click(self, template_path, threshold=0.7):
        """Find and click on a template image"""
        template = self.template_cache.get(template_path)
        if template is None:
            print(f"Template not found in cache: {template_path}")
            return False

        screen = self.take_screenshot()

        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            print(f"Found {template_path}, max_val: {max_val}")
            h, w = template.shape[:2]
            center_x = max_loc[0] + w//2
            center_y = max_loc[1] + h//2

            rand_x, rand_y = self.add_random_offset(center_x, center_y)
            self.adb_command(
                ['shell', 'input', 'tap', str(rand_x), str(rand_y)])
            return True
        print(f"Didn't find {template_path}, max_val: {max_val}")
        return False

    def click_coordinates(self, coords):
        """Click on specified coordinates with random offset"""
        rand_x, rand_y = self.add_random_offset(coords['x'], coords['y'])
        self.adb_command(['shell', 'input', 'tap', str(rand_x), str(rand_y)])

    def get_template_paths(self):
        """Get all PNG files from templates directory"""
        template_pattern = os.path.join(self.TEMPLATES_DIR, '*.png')
        return glob.glob(template_pattern)

    def add_random_delay(self, base_delay, variation_percent=20):
        """Add a random delay variation"""
        variation = base_delay * (variation_percent / 100)
        return base_delay + random.uniform(-variation, variation)

    def process_village(self, templates):
        """Process a single village's scouting routine"""
        self.click_coordinates(
            self.GAME_COORDS['MIDDLE_OF_SCREEN'])
        time.sleep(self.add_random_delay(1))
        self.click_coordinates(
            self.GAME_COORDS['MIDDLE_OF_SCREEN'])
        time.sleep(self.add_random_delay(1))

        for template_path in templates:
            if self.find_and_click(template_path):
                print(f"Clicked template: {os.path.basename(template_path)}")

                time.sleep(self.add_random_delay(1))
                if self.find_and_click('SCOUT_BUTTON'):
                    time.sleep(self.add_random_delay(1))
                    self.find_and_click('GO_BUTTON')
                    time.sleep(self.add_random_delay(1))
                    if self.find_and_click('SCOUT_EXIT_BUTTON'):
                        time.sleep(self.add_random_delay(2))
                    return True

            else:
                print(f"Template not found: {os.path.basename(template_path)}")

        return False

    def run(self):
        """Main loop to run the bot with Ctrl+C handling"""
        try:
            templates = self.get_template_paths()
            if not templates:
                print(f"No template images found in {self.TEMPLATES_DIR}")
                return

            print(
                f"Found {len(templates)} templates: {[os.path.basename(t) for t in templates]}")

            cooldown_time = 60 * 2
            last_click = None

            while True:
                current_time = datetime.now()

                if last_click is not None and current_time - last_click < timedelta(seconds=cooldown_time):
                    remaining = (
                        last_click + timedelta(seconds=cooldown_time) - current_time).seconds
                    print(f"In cooldown. {remaining} seconds remaining")
                    time.sleep(self.add_random_delay(2))
                    continue

                time.sleep(self.add_random_delay(2))

                for i in range(self.number_of_villages):
                    if i != 0:
                        self.click_coordinates(
                            self.GAME_COORDS['NEXT_VILLAGE'])
                        time.sleep(self.add_random_delay(2))
                        self.click_coordinates(self.GAME_COORDS['HOME_BUTTON'])
                        time.sleep(self.add_random_delay(2))

                    print(f"\nProcessing Village {i + 1}")
                    if self.process_village(templates):
                        last_click = current_time
                        print(f"Successfully processed Village {i + 1}")
                    else:
                        print(f"No action needed for Village {i + 1}")

                    time.sleep(self.add_random_delay(2))

                self.click_coordinates(self.GAME_COORDS['NEXT_VILLAGE'])
                time.sleep(self.add_random_delay(2))
                self.click_coordinates(self.GAME_COORDS['HOME_BUTTON'])
                time.sleep(self.add_random_delay(2))

        except KeyboardInterrupt:
            print("\nBot stopped by user (Ctrl+C)")
            print("Cleaning up and exiting...")
            sys.exit(0)
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            raise


if __name__ == "__main__":
    bot = StrongholdBot()
    bot.run()
