import re
from subprocess import Popen, PIPE
from services.config_service import ConfigService
import shutil


class TouchMonitor:
    def __init__(self):
        self.config_service = ConfigService()
        config = self.config_service.load_config()
        self.device_address = config['device_address']
        self.screen_width, self.screen_height = self.get_screen_resolution()
        self.TOUCH_MAX_X = 32767  # Typical max X coordinate for touch panels
        self.TOUCH_MAX_Y = 32767  # Typical max Y coordinate for touch panels
        self.touch_device = self.find_touch_device()

    def get_screen_resolution(self):
        """Fetch the screen resolution from the device using adb."""
        cmd = ['adb', '-s', self.device_address, 'shell', 'wm', 'size']
        process = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        output = process.communicate()[0]
        match = re.search(r'(\d+)x(\d+)', output)
        if match:
            return int(match.group(1)), int(match.group(2))
        return 1920, 1080  # Default fallback resolution

    def find_touch_device(self):
        """Identify the touch input device dynamically."""
        cmd = ['adb', '-s', self.device_address, 'shell', 'getevent', '-lp']
        process = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        output, _ = process.communicate()

        current_device = None
        for line in output.splitlines():
            if line.startswith("add device"):
                current_device = line.split(":")[1].strip()
            if "ABS_MT_POSITION_X" in line or "ABS_MT_POSITION_Y" in line:
                print(f"Detected touch device: {current_device}")
                return current_device

        raise RuntimeError("No suitable touch device found.")

    def monitor_touches(self):
        """Monitor touch events and print the screen coordinates."""
        if not self.touch_device:
            print("No touch device found.")
            return

        cmd = ['adb', '-s', self.device_address, 'shell',
               'getevent', '-lt', self.touch_device]
        process = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)

        x = None
        y = None

        print("Monitoring for clicks... Press Ctrl+C to stop")
        try:
            while True:
                line = process.stdout.readline().strip()
                if 'ABS_MT_POSITION_X' in line:
                    raw_x = int(line.split()[-1], 16)
                    x = int((raw_x / self.TOUCH_MAX_X) * self.screen_width)
                elif 'ABS_MT_POSITION_Y' in line:
                    raw_y = int(line.split()[-1], 16)
                    y = int((raw_y / self.TOUCH_MAX_Y) * self.screen_height)
                    if x is not None:
                        print(f"Click detected at: {{'x': {x}, 'y': {y}}}")
                        x = None
                        y = None
        except KeyboardInterrupt:
            process.kill()
            print("\nMonitoring stopped")

    def connect_device(self):
        """Connect to the specified device using adb."""
        Popen(['adb', 'connect', self.device_address]).wait()


def get_terminal_size():
    try:
        columns, rows = shutil.get_terminal_size()
    except:
        columns, rows = 80, 24
    return columns, rows


def create_box(width):
    # Characters for box drawing
    top_left = "╔"
    top_right = "╗"
    bottom_left = "╚"
    bottom_right = "╝"
    horizontal = "═"
    vertical = "║"
    left_separator = "╠"
    right_separator = "╣"

    # Calculate usable width (content area)
    content_width = width - 2  # Subtract 2 for left and right borders

    def create_line(text, padding_left=2):
        # Left-aligned text with specified padding
        if len(text) + padding_left > content_width:
            text = text[:content_width - padding_left]
        padded_text = " " * padding_left + text
        return f"{vertical}{padded_text}{' ' * (content_width - len(padded_text))}{vertical}"

    # Create box with dynamic width
    box = [
        f"{top_left}{horizontal * content_width}{top_right}",
        create_line("Coordinate Recording Tool", 1),
        f"{left_separator}{horizontal * content_width}{right_separator}",
        create_line(
            "This script helps record coordinates for config.json fields:"),
        create_line("• village_1_parish_coords"),
        create_line("• parish_trade_button_coords"),
        create_line(""),
        create_line("Instructions:"),
        create_line("1. Click on the desired location on emulator 5-10 times"),
        create_line("2. Coordinates will be logged in this format:"),
        create_line("   Click detected at: {'x': 123, 'y': 456}"),
        f"{bottom_left}{horizontal * content_width}{bottom_right}"
    ]

    return "\n".join(box)


def show_instructions():
    terminal_width, _ = get_terminal_size()
    box_width = max(60, min(terminal_width, 80))
    print(f"\n{create_box(box_width)}\n")


if __name__ == "__main__":
    show_instructions()

    monitor = TouchMonitor()
    monitor.connect_device()
    monitor.monitor_touches()
