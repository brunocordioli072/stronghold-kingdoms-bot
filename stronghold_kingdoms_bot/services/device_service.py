import cv2
from subprocess import run
import numpy as np
from stronghold_kingdoms_bot.services.template_service import TemplateService
from time import sleep
import pytesseract


class DeviceService:
    """Controls and interacts with Android devices using ADB"""

    def __init__(self, device_address, template_service: TemplateService):
        """Sets up connection to device and initializes template service"""
        self.device_address = device_address
        self.template_service = template_service
        self.connect_device()

    def connect_device(self):
        """Connects to the device using ADB"""
        run(['adb', 'connect', self.device_address])

    def adb_command(self, command):
        """Runs an ADB command on the device"""
        return run(['adb', '-s', self.device_address] + command, capture_output=True)

    def take_screenshot(self):
        """Takes a screenshot of the device screen"""
        self.adb_command(['shell', 'screencap', '-p', '/sdcard/screen.png'])
        self.adb_command(['pull', '/sdcard/screen.png', '.'])
        return cv2.imread('screen.png')

    def tap(self, x, y):
        """Taps the screen at given coordinates"""
        self.adb_command(['shell', 'input', 'tap', str(x), str(y)])

    def add_random_offset(self, x, y, max_radius=1):
        """Adds small random offset to coordinates to make taps look more human"""
        offset_x = int(np.random.normal(0, max_radius/3))
        offset_y = int(np.random.normal(0, max_radius/3))

        offset_x = max(min(offset_x, max_radius), -max_radius)
        offset_y = max(min(offset_y, max_radius), -max_radius)

        return x + offset_x, y + offset_y

    def find_and_click_template(self, template_path, threshold=None):
        """Finds a template image on screen and clicks it if found, with edge detection."""
        t = self.template_service.get_template(template_path)
        template = t["img"]
        if template is None:
            print(f"Template not found in cache: {template_path}")
            return False

        image = self.take_screenshot()

        # Convert to HSV for color-based filtering
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define color ranges for masks
        gray_lower = np.array([0, 0, 50])
        gray_upper = np.array([180, 50, 200])
        blue_lower = np.array([90, 50, 50])
        blue_upper = np.array([130, 255, 255])
        white_lower = np.array([0, 0, 200])
        white_upper = np.array([180, 50, 255])
        green_lower = np.array([25, 100, 50])
        green_upper = np.array([35, 255, 255])

        # Create masks
        gray_mask = cv2.inRange(hsv, gray_lower, gray_upper)
        blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
        white_mask = cv2.inRange(hsv, white_lower, white_upper)
        green_mask = cv2.inRange(hsv, green_lower, green_upper)

        # Combine masks for background
        background_mask = cv2.bitwise_or(blue_mask, gray_mask)
        background_mask = cv2.bitwise_or(background_mask, white_mask)
        background_mask = cv2.bitwise_or(background_mask, green_mask)

        # Create menu mask and apply it
        menu_mask = np.zeros_like(background_mask)
        # Define regions for menus
        regions = [
            [0, 0, 100, 200],
            [image.shape[1] - 350, 0, 350, 170],
            [0, image.shape[0] - 150, 100, 150],
            [image.shape[1] - 100, image.shape[0] - 150, 100, 150],
            [image.shape[1] // 2 - 70, image.shape[0] // 2 - 70, 155, 155],
            [image.shape[1] // 2 - 125, image.shape[0] - 80, 255, 80],
        ]
        for x, y, w, h in regions:
            cv2.rectangle(menu_mask, (x, y), (x + w, y + h), 255, -1)

        # Combine masks and invert to isolate icons
        background_mask = cv2.bitwise_or(background_mask, menu_mask)
        icons_mask = cv2.bitwise_not(background_mask)

        # Apply mask to isolate icons
        icons_only = cv2.bitwise_and(image, image, mask=icons_mask)

        # Convert to grayscale for edge detection
        gray_icons = cv2.cvtColor(icons_only, cv2.COLOR_BGR2GRAY)
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # Apply Canny edge detection
        # Adjust thresholds as needed
        edges_icons = cv2.Canny(gray_icons, 50, 150)

        # Save the edge-detected images for debugging
        cv2.imwrite('processed_image.png', edges_icons)

        # Match template using edge-detected images
        result = cv2.matchTemplate(
            edges_icons, gray_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        effective_threshold = threshold if threshold is not None else t['threshold']
        if max_val >= effective_threshold:
            print(f"Found {template_path}, max_val: {max_val}")
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            rand_x, rand_y = self.add_random_offset(center_x, center_y)
            self.tap(rand_x, rand_y)
            return True

        print(f"Didn't find {template_path}, max_val: {max_val}")
        return False

    def find_and_click(self, template_path, threshold=None):
        """Finds a template image on screen and clicks it if found"""
        t = self.template_service.get_template(template_path)
        template = t["img"]
        if template is None:
            print(f"Template not found in cache: {template_path}")
            return False

        screen = self.take_screenshot()

        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        CANT_CLICK_AREAS = [
            {'top_left': {'x': 582, 'y': 775},
                'bottom_right': {'x': 1022, 'y': 892}},
            {'top_left': {'x': 0, 'y': 2}, 'bottom_right': {'x': 101, 'y': 200}},
            {'top_left': {'x': 2, 'y': 791}, 'bottom_right': {'x': 104, 'y': 891}},
            {'top_left': {'x': 1256, 'y': 0}, 'bottom_right': {'x': 1590, 'y': 53}},
            {'top_left': {'x': 1439, 'y': 52},
                'bottom_right': {'x': 1591, 'y': 108}},
            {'top_left': {'x': 1529, 'y': 108},
                'bottom_right': {'x': 1593, 'y': 161}},
        ]

        effective_threshold = threshold if threshold is not None else t['threshold']

        if max_val >= effective_threshold:
            print(f"Found {template_path}, max_val: {max_val}")
            h, w = template.shape[:2]
            center_x = max_loc[0] + w//2
            center_y = max_loc[1] + h//2
            for area in CANT_CLICK_AREAS:
                if (area['top_left']['x'] <= center_x <= area['bottom_right']['x'] and
                        area['top_left']['y'] <= center_y <= area['bottom_right']['y']):
                    print(
                        f"Can't be clicked. Coords ({center_x}, {center_y}) are in a restricted area.")
                    return False
            rand_x, rand_y = self.add_random_offset(center_x, center_y)
            self.tap(rand_x, rand_y)

            return True
        print(f"Didn't find {template_path}, max_val: {max_val}")
        return False

    def find_and_click_and_sleep(self, template_path, threshold=0.7, sleep=1):
        """Finds and clicks a template image, then waits for specified time"""
        t = self.template_service.get_template(template_path)
        template = t["img"]
        if template is None:
            print(f"Template not found in cache: {template_path}")
            return False

        screen = self.take_screenshot()

        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= t['threshold']:
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
        """Clicks at given coordinates with slight random offset"""
        rand_x, rand_y = self.add_random_offset(coords['x'], coords['y'])
        self.tap(rand_x, rand_y)

    def click_coordinates_and_sleep(self, coords, sleep=1):
        """Clicks at coordinates and waits for specified time"""
        rand_x, rand_y = self.add_random_offset(coords['x'], coords['y'])
        self.tap(rand_x, rand_y)
        self.sleep(sleep)

    def add_random_delay(self, base_delay, variation_percent=20):
        """Adds random variation to a delay time"""
        variation = base_delay * (variation_percent / 100)
        return base_delay + np.random.uniform(-variation, variation)

    def sleep(self, time):
        """Waits for specified time with slight random variation"""
        sleep(self.add_random_delay(time))

    def get_numbers_from_coords(self, coords1, coords2, name=None):
        """Extracts numbers from a specific area of the screen"""
        screen = self.take_screenshot()
        cropped_image = screen[coords1['y']:coords2['y'],
                               coords1['x']:coords2['x']]
        custom_config = r'--psm 6 -c tessedit_char_whitelist=0123456789'

        text = pytesseract.image_to_string(cropped_image, config=custom_config)
        return text

    def get_text_from_coords(self, coords1, coords2):
        """Extracts text from a specific area of the screen with improved recognition"""

        # Take screenshot and crop the region of interest
        screen = self.take_screenshot()
        cropped_image = screen[coords1['y']:coords2['y'],
                               coords1['x']:coords2['x']]

        # Convert to grayscale
        gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to get black text on white background
        _, binary = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Increase image size to improve recognition
        scaled = cv2.resize(binary, None, fx=2, fy=2,
                            interpolation=cv2.INTER_CUBIC)

        # Apply slight gaussian blur to reduce noise
        denoised = cv2.GaussianBlur(scaled, (3, 3), 0)

        # Configure Tesseract parameters for better recognition
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ãõáéíóúâêîôûàèìòù/'

        # Perform OCR
        text = pytesseract.image_to_string(denoised, config=custom_config)

        return text.strip()
