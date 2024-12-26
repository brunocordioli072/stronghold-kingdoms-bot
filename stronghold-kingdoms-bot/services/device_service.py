import cv2
from subprocess import run
import numpy as np
from services.template_service import TemplateService
from time import sleep


class DeviceService:
    def __init__(self, device_id, template_service: TemplateService):
        self.device_id = device_id
        self.template_service = template_service
        self.connect_device()

    def connect_device(self):
        """Connect to the specified device using ADB"""
        run(['adb', 'connect', self.device_id])

    def adb_command(self, command):
        """Run ADB command for the device"""
        return run(['adb', '-s', self.device_id] + command, capture_output=True)

    def take_screenshot(self):
        """Take and return a screenshot from the device"""
        self.adb_command(['shell', 'screencap', '-p', '/sdcard/screen.png'])
        self.adb_command(['pull', '/sdcard/screen.png', '.'])
        return cv2.imread('screen.png')

    def tap(self, x, y):
        """Tap on the specified coordinates"""
        self.adb_command(['shell', 'input', 'tap', str(x), str(y)])

    def add_random_offset(self, x, y, max_radius=5):
        """Add a random offset to coordinates within a specified radius"""
        offset_x = int(np.random.normal(0, max_radius/3))
        offset_y = int(np.random.normal(0, max_radius/3))

        offset_x = max(min(offset_x, max_radius), -max_radius)
        offset_y = max(min(offset_y, max_radius), -max_radius)

        return x + offset_x, y + offset_y

    def find_and_click(self, template_path, threshold=0.7):
        """Find and click on a template image"""
        template = self.template_service.get_template(template_path)
        if template is None:
            print(f"Template not found in cache: {template_path}")
            return False

        screen = self.take_screenshot()

        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        CANT_CLICK_TOP_LEFT = {'x': 582, 'y': 775}
        CANT_CLICK_BOTTOM_RIGHT = {'x': 1022, 'y': 892}

        if max_val >= threshold:
            print(f"Found {template_path}, max_val: {max_val}")
            h, w = template.shape[:2]
            center_x = max_loc[0] + w//2
            center_y = max_loc[1] + h//2
            if (CANT_CLICK_TOP_LEFT['x'] <= center_x <= CANT_CLICK_BOTTOM_RIGHT['x'] and
                    CANT_CLICK_TOP_LEFT['y'] <= center_y <= CANT_CLICK_BOTTOM_RIGHT['y']):
                print(f'Can\'t be clicked. Coords on bad position.')
                return False
            rand_x, rand_y = self.add_random_offset(center_x, center_y)
            self.tap(rand_x, rand_y)
            return True
        print(f"Didn't find {template_path}, max_val: {max_val}")
        return False

    def find_and_click_and_sleep(self, template_path, threshold=0.7, sleep=1):
        """Find and click on a template image"""
        template = self.template_service.get_template(template_path)
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
            self.tap(rand_x, rand_y)
            self.sleep(sleep)
            return True
        print(f"Didn't find {template_path}, max_val: {max_val}")
        self.sleep(sleep)
        return False

    def click_coordinates(self, coords):
        """Click on specified coordinates with random offset"""
        rand_x, rand_y = self.add_random_offset(coords['x'], coords['y'])
        self.tap(rand_x, rand_y)

    def click_coordinates_and_sleep(self, coords, sleep=1):
        rand_x, rand_y = self.add_random_offset(coords['x'], coords['y'])
        self.tap(rand_x, rand_y)
        self.sleep(sleep)

    def add_random_delay(self, base_delay, variation_percent=20):
        """Add a random delay variation"""
        variation = base_delay * (variation_percent / 100)
        return base_delay + np.random.uniform(-variation, variation)

    def sleep(self, time):
        sleep(self.add_random_delay(time))
