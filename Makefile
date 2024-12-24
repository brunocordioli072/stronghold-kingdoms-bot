# Target to run the main bot script
# This will execute the bot located in the "stronghold-kingdoms-bot" directory
run:
	python stronghold-kingdoms-bot/main.py

# Target to test the coordinates on emulator
# This script is useful for debugging and verifying screen coordinates
coords:
	python stronghold-kingdoms-bot/coordinates.py