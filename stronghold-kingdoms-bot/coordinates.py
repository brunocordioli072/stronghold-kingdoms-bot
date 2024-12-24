import re
from subprocess import Popen, PIPE
from config import ConfigService


class TouchMonitor:
    def __init__(self):
        self.config_service = ConfigService()
        config = self.config_service.load_config()
        self.device_id = config['device_id']
        self.screen_width, self.screen_height = self.get_screen_resolution()
        self.TOUCH_MAX_X = 32767  # Typical max X coordinate for touch panels
        self.TOUCH_MAX_Y = 32767  # Typical max Y coordinate for touch panels

    def get_screen_resolution(self):
        """Fetch the screen resolution from the device using adb."""
        cmd = ['adb', '-s', self.device_id, 'shell', 'wm', 'size']
        process = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        output = process.communicate()[0]
        match = re.search(r'(\d+)x(\d+)', output)
        if match:
            return int(match.group(1)), int(match.group(2))
        return 1920, 1080  # Default fallback resolution

    def monitor_touches(self):
        """Monitor touch events and print the screen coordinates."""
        cmd = ['adb', '-s', self.device_id, 'shell',
               'getevent', '-lt', '/dev/input/event4']
        process = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)

        x = None
        y = None

        print("Monitoring for clicks... Press Ctrl+C to stop")
        try:
            while True:
                line = process.stdout.readline().strip()
                if 'ABS_MT_POSITION_X' in line:
                    raw_x = int(line.split()[-1], 16)
                    # Convert raw X to screen X
                    x = int((raw_x / self.TOUCH_MAX_X) * self.screen_width)
                elif 'ABS_MT_POSITION_Y' in line:
                    raw_y = int(line.split()[-1], 16)
                    # Convert raw Y to screen Y
                    y = int((raw_y / self.TOUCH_MAX_Y) * self.screen_height)
                    if x is not None:
                        print(f"Click detected at: X={x}, Y={y}")
                        x = None
                        y = None
        except KeyboardInterrupt:
            process.kill()
            print("\nMonitoring stopped")

    def connect_device(self):
        """Connect to the specified device using adb."""
        Popen(['adb', 'connect', self.device_id]).wait()


if __name__ == "__main__":
    monitor = TouchMonitor()
    monitor.connect_device()
    monitor.monitor_touches()
