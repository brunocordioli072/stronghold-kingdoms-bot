# Stronghold Kingdoms Bot

This project is a bot designed to automate scouting routines in the game **Stronghold Kingdoms**. It interacts with a BlueStacks emulator instance via ADB (Android Debug Bridge) to perform specific tasks like clicking on predefined locations and templates.

## Features
- Automatically processes villages for scouting.
- Uses image recognition (via OpenCV) to identify and interact with game elements.
- Adds random offsets to clicks for more natural interactions.
- Introduces randomized delays between actions to mimic human behavior.

## Requirements

- Python 3.6+
- [ADB (Android Debug Bridge)](https://developer.android.com/studio/command-line/adb)
- [BlueStacks](https://www.bluestacks.com/) emulator installed and running.
- Required Python libraries:
  - `opencv-python`
  - `numpy`

You can install the required Python libraries with:
```bash
pip install -r ./requirements.txt
```

## Directory Structure

- `templates_bags/` - Directory containing template images used for identifying in-game elements.
- `templates_general/` - Directory containing additional templates (e.g., scout button, go button).
- `stronghold_kingdoms_bot.py` - Main bot script.

## Setup

1. Install BlueStacks and launch the Stronghold Kingdoms app.
2. Connect ADB to the BlueStacks instance:
    ```bash
    adb connect 127.0.0.1:5565
    ```
3. Place all required template images in the `templates_bags` and `templates_general` directories.
4. Update the `DEVICE_ID` variable in the script to match your BlueStacks instance address (default: `127.0.0.1:5565`).

## Usage

1. Run the script:
    ```bash
    python stronghold_kingdoms_bot.py
    ```
2. The bot will:
    - Iterate through villages in the game.
    - Perform scouting actions based on template matches.
    - Wait for a cooldown period (default: 15 minutes) before processing again.

## Configuration

- **Game Coordinates**: Update the `GAME_COORDS` dictionary with the correct screen coordinates for the `NEXT_VILLAGE` and `HOME_BUTTON` buttons in your game.
- **Cooldown Time**: Modify the `cooldown_time` variable in seconds to set the delay between scouting cycles (default: 15 minutes).
- **Randomization**: Adjust `max_radius` in the `add_random_offset` function and `variation_percent` in the `add_random_delay` function to control the randomness of clicks and delays.

## Logging

The script outputs log messages to the console, indicating:
- Templates found and clicked.
- Villages processed.
- Cooldown periods.

## Notes

- Ensure the templates match the in-game elements as closely as possible for accurate image recognition.
- The script assumes a consistent screen resolution and layout. If your BlueStacks instance has a different configuration, update the template images and coordinates accordingly.

## License

This project is for personal use and is provided "as is" without any warranty. Use at your own risk.

## Disclaimer

Using bots in games may violate the game's terms of service. The author is not responsible for any consequences resulting from the use of this bot.
