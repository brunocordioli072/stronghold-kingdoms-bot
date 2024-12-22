from subprocess import Popen, PIPE
import re

DEVICE_ID = "127.0.0.1:5565"  # BlueStacks instance

# Get the screen resolution from adb


def get_screen_resolution():
    cmd = ['adb', '-s', DEVICE_ID, 'shell', 'wm', 'size']
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    output = process.communicate()[0]
    match = re.search(r'(\d+)x(\d+)', output)
    if match:
        return int(match.group(1)), int(match.group(2))
    return 1920, 1080  # default fallback resolution


def monitor_touches():
    # Get screen resolution
    screen_width, screen_height = get_screen_resolution()

    # Constants for coordinate conversion (typical touch panel resolution)
    TOUCH_MAX_X = 32767
    TOUCH_MAX_Y = 32767

    cmd = ['adb', '-s', DEVICE_ID, 'shell',
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
                x = int((raw_x / TOUCH_MAX_X) * screen_width)
            elif 'ABS_MT_POSITION_Y' in line:
                raw_y = int(line.split()[-1], 16)
                # Convert raw Y to screen Y
                y = int((raw_y / TOUCH_MAX_Y) * screen_height)
                if x is not None:
                    print(f"Click detected at: X={x}, Y={y}")
                    x = None
                    y = None
    except KeyboardInterrupt:
        process.kill()
        print("\nMonitoring stopped")


if __name__ == "__main__":
    # First connect to the device
    Popen(['adb', 'connect', DEVICE_ID]).wait()
    monitor_touches()
