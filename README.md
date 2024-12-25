<div align="center">
<p align="center">
<img src="https://github.com/user-attachments/assets/24a479cf-1770-49ab-b079-2cb233a6112b">
</p>

<h1 align="center">
Stronghold Kingdoms Bot
</h1>

[![GitHub Stars](https://img.shields.io/github/stars/brunocordioli072/stronghold-kingdoms-bot?style=flat-square)](https://github.com/brunocordioli072/stronghold-kingdoms-bot/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/brunocordioli072/stronghold-kingdoms-bot?style=flat-square)](https://github.com/brunocordioli072/stronghold-kingdoms-bot/network)
[![GitHub Issues](https://img.shields.io/github/issues/brunocordioli072/stronghold-kingdoms-bot?style=flat-square)](https://github.com/brunocordioli072/stronghold-kingdoms-bot/issues)
[![GitHub Contributors](https://img.shields.io/github/contributors/brunocordioli072/stronghold-kingdoms-bot?style=flat-square)](https://github.com/brunocordioli072/stronghold-kingdoms-bot/graphs/contributors)
[![GitHub License](https://img.shields.io/github/license/brunocordioli072/stronghold-kingdoms-bot?style=flat-square)](https://github.com/brunocordioli072/stronghold-kingdoms-bot/blob/main/LICENSE)
</div>

## Disclaimer

This software is an external tool designed to automate playing Stronghold Kingdoms. It is designed to interact with the game only through existing user interfaces and comply with relevant laws and regulations. The package aims to provide simplified and user-friendly interaction with the game, and it is not intended to disrupt game balance in any way or provide any unfair advantages. The package will not modify any game files or game code in any way.

This software is open source, free of charge, and for learning and exchange purposes only. The developer team has the final right to interpret this project. All problems arising from the use of this software are not related to this project and the developer team. If you encounter a merchant using this software to practice on your behalf and charging for it, it may be the cost of equipment and time, etc. The problems and consequences arising from this software have nothing to do with it.

## About

A Python bot that automates actions in the game using ADB (Android Debug Bridge). It connects to a device, processes villages, and performs predefined actions like scouting.

## Requirements
- Python 3.x
- ADB installed and in your PATH
- BlueStacks or another emulator with ADB enabled
- Tesseract and in your PATH

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
