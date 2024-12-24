import cv2
from subprocess import run


class DeviceService:
    def __init__(self, device_id):
        self.device_id = device_id
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
