# Stronghold Bot

A Python bot that automates actions in the game using ADB (Android Debug Bridge). It connects to a device, processes villages, and performs predefined actions like scouting.

## Requirements
- Python 3.x
- ADB installed and in your PATH
- BlueStacks or another emulator with ADB enabled

## Setup
1. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

2. Ensure ADB is set up and the device is running.

3. Run the bot:
   ```sh
   python ./main.py
   ```

4. Edit `config.json` with your device ID and number of villages if needed.
5. Install tesseract https://github.com/tesseract-ocr/tesseract/releases/latest and add it to path

## Usage
The bot will:
1. Connect to the specified device.
2. Process each village, performing actions based on image templates.
3. Repeat for all villages with cooldowns in between.

## Notes
- Place your template images in the `templates_bags` folder.
- Adjust the `config.json` file for your setup.
- Install tesseract https://github.com/tesseract-ocr/tesseract/releases/latest and add it to path

## Stopping the Bot
Press `Ctrl+C` to stop the bot safely.

## Disclaimer
This bot is intended for educational purposes only. The developers and contributors are not responsible for any misuse, including violations of game terms of service or local laws. Use at your own risk and ensure compliance with applicable regulations.
