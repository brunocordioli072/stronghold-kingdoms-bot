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


class StrongholdBot:
    def __init__(self, device_id=None, number_of_villages=None, config_file="config.json", base_path=None):
        # Set base_path to project root, not the script directory
        self.base_path = base_path or os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..'))  # Go up one level

        self.config_service = ConfigService()
        self.template_service = TemplateService(self.base_path)

        self.GAME_COORDS = {
            'NEXT_VILLAGE': {'x': 970, 'y': 809},
            'HOME_BUTTON': {'x': 1554, 'y': 762},
            'MIDDLE_OF_SCREEN': {'x': 794, 'y': 439},
        }

        if device_id and number_of_villages:
            self.device_id = device_id
            self.number_of_villages = number_of_villages
        else:
            config = self.config_service.load_config()
            self.device_id = config['device_id']
            self.number_of_villages = config['number_of_villages']

        self.device_service = DeviceService(self.device_id)

        # Cache templates
        self.template_service.cache_templates()

    def add_random_offset(self, x, y, max_radius=5):
        """Add a random offset to coordinates within a specified radius"""
        offset_x = int(np.random.normal(0, max_radius/3))
        offset_y = int(np.random.normal(0, max_radius/3))

        offset_x = max(min(offset_x, max_radius), -max_radius)
        offset_y = max(min(offset_y, max_radius), -max_radius)

        return x + offset_x, y + offset_y

    def find(self, template_path, threshold=0.7):
        """Find and click on a template image"""
        template = self.template_service.get_template(template_path)
        if template is None:
            print(f"Template not found in cache: {template_path}")
            return False

        screen = self.device_service.take_screenshot()

        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            print(f"Found {template_path}, max_val: {max_val}")
            return True
        print(f"Didn't find {template_path}, max_val: {max_val}")
        return False

    def find_and_click(self, template_path, threshold=0.7):
        """Find and click on a template image"""
        template = self.template_service.get_template(template_path)
        if template is None:
            print(f"Template not found in cache: {template_path}")
            return False

        screen = self.device_service.take_screenshot()

        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            print(f"Found {template_path}, max_val: {max_val}")
            h, w = template.shape[:2]
            center_x = max_loc[0] + w//2
            center_y = max_loc[1] + h//2

            rand_x, rand_y = self.add_random_offset(center_x, center_y)
            self.device_service.tap(rand_x, rand_y)
            return True
        print(f"Didn't find {template_path}, max_val: {max_val}")
        return False

    def click_coordinates(self, coords):
        """Click on specified coordinates with random offset"""
        rand_x, rand_y = self.add_random_offset(coords['x'], coords['y'])
        self.device_service.tap(rand_x, rand_y)

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
            templates = self.template_service.get_template_bags_paths()
            if not templates:
                print(
                    f"No template images found in {self.template_service.TEMPLATES_DIR}")
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
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..'))
    bot = StrongholdBot(base_path=project_root)
    bot.run()
