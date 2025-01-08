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

## Requirements
- [Android Debug Bridge](https://community.chocolatey.org/packages/adb)
- [Tesseract Open Source OCR Engine](https://community.chocolatey.org/packages/tesseract)
- [Python](https://community.chocolatey.org/packages/python#)
- [GNU Make](https://community.chocolatey.org/packages/make)


# Stronghold Kingdoms Bot

A bot for automating Stronghold Kingdoms gameplay in Android emulators.


# Getting Started

## Quick Install

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/brunocordioli072/stronghold-kingdoms-bot/main/scripts/install.ps1" -OutFile "./install.ps1"; &"./install.ps1"
```

## Manual Setup

1. Install Chocolatey https://chocolatey.org/install#individual.
    - Chocolatey is a package manager for Windows. It is easier to install the needed dependencies with it.
2. Install Android Debug Bridge by running `choco install adb` on your terminal as admin.
    - Android Debug Bridge is command-line tool that enable communication with a device. It enables to send inputs directly to the emulator.
3. Install Tesseract Open Source OCR Engine by running `choco install tesseract` on your terminal as admin.
    - Tesseract is a free, open-source Optical Character Recognition (OCR) engine that converts images of text into machine-readable text.
4. Install Python by running `choco install python --pre` on your terminal as admin.
    - The programming language used for the project.
5. Install GNU Make by running `choco install make` on your terminal as admin.
    - GNU Make is a tool that automates the process of building and managing software projects.
6. Enable Android Debug Bridge on your emulator. **(Bluestacks is recommended.)**
    - Bluestacks: Settings > Advanced > Enable Android Debug Bridge.
7. Go to Stronghold Kingdoms app > Menu > Settings > Set User Interface Size > Set to minimum
8. Clone the repo by running `git clone https://github.com/brunocordioli072/stronghold-kingdoms-bot`.
9. Install the repo dependencies by running `pip install -r ./requirements.txt`
10. To use the bot, run `make run` on the root folder of the `stronghold-kingdoms-bot` with the Stronghold Kingdoms app open on Emulator.

## Configuration

The first time the bot is run it will create a `config.json` on the root folder of the `stronghold-kingdoms-bot` that looks like this:
```json
{
   "device_address": "127.0.0.1:your-port",
   "number_of_villages": 1,
   "interval_between_loop_in_seconds": 240,
   "village_1_name": "YourVillageName",
   "village_1_parish_coords": {
      "x": 1,
      "y": 1
   },
   "parish_trade_button_coords": {
      "x": 1,
      "y": 1
   },
   "sell": {
      "foods": {
         "apple": true,
         "cheese": true,
         "meat": true,
         "bread": true,
         "veggies": true,
         "fish": true,
         "ale": true
      },
      "luxury": {
         "venison": true,
         "furniture": true,
         "metalware": true,
         "clothes": true,
         "wine": true,
         "salt": true,
         "spices": true,
         "silk": true
      }
   }
}
```
You will need to replace these fields with the correct values. After that, run again `make run`, and the bot should start.
Meaning of each field:
- device_address: Address of the device.
- number_of_villages: Number of villages the player has.
- interval_between_loop_in_seconds: This is the waiting time the bot has after doing the scouting and trading.
- village_1_name: Your first village name. No special characters.
- village_1_parish_coords: Coordinates of the village 1 parish. Use `make coords` to get this coordinates.
- parish_trade_button_coords: Coordinates of trade button on parish menu. Use `make coords` to get this coordinates.
- sell: Configuration for selling products on parish. Set `false` on product if you don't want to sell it.

## Contributors

Thanks to the following contributors for their contributions to this project.

<a href="https://github.com/brunocordioli072/stronghold-kingdoms-bot/graphs/contributors">

  <img src="https://contrib.rocks/image?repo=brunocordioli072/stronghold-kingdoms-bot" />

</a>
