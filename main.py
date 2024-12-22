import cv2
import numpy as np
from subprocess import run
import time
from datetime import datetime, timedelta
import os
import glob
import random

DEVICE_ID = "127.0.0.1:5565"  # Specific BlueStacks instance
TEMPLATES_DIR = 'C:\\Users\\kurtz\\work\\stronghold-kingdoms-bot\\templates_bags'

GAME_COORDS = {
    'NEXT_VILLAGE': {'x': 970, 'y': 809},  # Button to open villages list
    'HOME_BUTTON': {'x': 1554, 'y': 762}
}


def add_random_offset(x, y, max_radius=5):
    """
    Add a random offset to coordinates within a specified radius.
    The offset follows a normal distribution to favor smaller deviations.

    Args:
        x (int): Original x coordinate
        y (int): Original y coordinate
        max_radius (int): Maximum pixel radius for randomization

    Returns:
        tuple: New (x, y) coordinates with random offset
    """
    # Use normal distribution for more natural randomization
    # Scale factor of 3 means ~99.7% of values fall within max_radius
    offset_x = int(np.random.normal(0, max_radius/3))
    offset_y = int(np.random.normal(0, max_radius/3))

    # Clamp values to max_radius
    offset_x = max(min(offset_x, max_radius), -max_radius)
    offset_y = max(min(offset_y, max_radius), -max_radius)

    return x + offset_x, y + offset_y


def adb_command(command):
    """Run ADB command for specific device"""
    return run(['adb', '-s', DEVICE_ID] + command, capture_output=True)


def take_screenshot():
    # Take screenshot using adb
    adb_command(['shell', 'screencap', '-p', '/sdcard/screen.png'])
    # Pull the screenshot to local machine
    adb_command(['pull', '/sdcard/screen.png', '.'])
    # Read the screenshot
    return cv2.imread('screen.png')


def find_and_click(template_path, threshold=0.7):
    # Read the template image we want to find
    template = cv2.imread(template_path)
    # Take screenshot of current screen
    screen = take_screenshot()

    # Perform template matching
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # If match found above threshold
    if max_val >= threshold:
        # Get center coordinates of the match
        h, w = template.shape[:2]
        center_x = max_loc[0] + w//2
        center_y = max_loc[1] + h//2

        # Add random offset to click coordinates
        rand_x, rand_y = add_random_offset(center_x, center_y)

        # Click on the randomized coordinates using adb
        adb_command(['shell', 'input', 'tap', str(rand_x), str(rand_y)])
        return True
    return False


def click_coordinates(coords):
    # Add random offset to the predefined coordinates
    rand_x, rand_y = add_random_offset(coords['x'], coords['y'])
    adb_command(['shell', 'input', 'tap', str(rand_x), str(rand_y)])


def get_template_paths():
    """Get all PNG files from templates directory"""
    template_pattern = os.path.join(TEMPLATES_DIR, '*.png')
    return glob.glob(template_pattern)


def add_random_delay(base_delay, variation_percent=20):
    """
    Add a random delay variation to the base delay time

    Args:
        base_delay (float): Base delay time in seconds
        variation_percent (int): Maximum percentage of variation

    Returns:
        float: Randomized delay time
    """
    variation = base_delay * (variation_percent / 100)
    return base_delay + random.uniform(-variation, variation)


def process_village(templates):
    """Process a single village's scouting routine"""

    for template_path in templates:
        if find_and_click(template_path):
            print(f"Clicked template: {os.path.basename(template_path)}")

            time.sleep(add_random_delay(1))
            SCOUT_BUTTON = 'C:\\Users\\kurtz\\work\\stronghold-kingdoms-bot\\templates_general\\scout_button.png'
            if find_and_click(SCOUT_BUTTON):
                time.sleep(add_random_delay(1))
                GO_BUTTON = 'C:\\Users\\kurtz\\work\\stronghold-kingdoms-bot\\templates_general\\go_button.png'
                if find_and_click(GO_BUTTON):
                    return True  # Successfully processed this village
        else:
            print(f"Template not found: {os.path.basename(template_path)}")

    return False  # No successful processing for this village


def main():
    # Connect to specific BlueStacks instance
    run(['adb', 'connect', DEVICE_ID])

    # Get list of template paths
    templates = get_template_paths()
    if not templates:
        print(f"No template images found in {TEMPLATES_DIR}")
        return

    print(
        f"Found {len(templates)} templates: {[os.path.basename(t) for t in templates]}")

    cooldown_time = 60 * 15  # Cooldown in seconds
    last_click = None

    while True:
        current_time = datetime.now()

        # Check if we're still in cooldown
        if last_click is not None and current_time - last_click < timedelta(seconds=cooldown_time):
            remaining = (
                last_click + timedelta(seconds=cooldown_time) - current_time).seconds
            print(f"In cooldown. {remaining} seconds remaining")
            time.sleep(add_random_delay(2))
            continue

        time.sleep(add_random_delay(2))

        # Process each village
        for i in range(4):
            if i != 0:
                click_coordinates(GAME_COORDS['NEXT_VILLAGE'])
                time.sleep(add_random_delay(2))
                click_coordinates(GAME_COORDS['HOME_BUTTON'])
                time.sleep(add_random_delay(2))

            print(f"\nProcessing Village {i + 1}")
            if process_village(templates):
                last_click = current_time
                print(f"Successfully processed Village {i + 1}")
            else:
                print(f"No action needed for Village {i + 1}")

            time.sleep(add_random_delay(2))  # Wait between villages

        click_coordinates(GAME_COORDS['NEXT_VILLAGE'])
        time.sleep(add_random_delay(2))
        click_coordinates(GAME_COORDS['HOME_BUTTON'])
        time.sleep(add_random_delay(2))  # Wait before next cycle


if __name__ == "__main__":
    main()
