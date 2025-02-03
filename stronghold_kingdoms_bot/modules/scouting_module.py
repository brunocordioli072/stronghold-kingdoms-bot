import os
import sys
from loguru import logger
from stronghold_kingdoms_bot.services.config_service import ConfigService
from stronghold_kingdoms_bot.services.template_service import TemplateService
from stronghold_kingdoms_bot.services.device_service import DeviceService
from stronghold_kingdoms_bot.services.utils_service import UtilsService

from subprocess import run
import cv2


class ScoutingModule:
    def __init__(self):
        self.base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..'))

        self.config_service = ConfigService()
        config = self.config_service.load_config()
        self.device_address = config['device_address']
        self.number_of_villages = config['number_of_villages']

        self.template_service = TemplateService(self.base_path)
        self.device_service = DeviceService(
            self.device_address, self.template_service)
        self.utils_service = UtilsService(self.device_service)

        self.GAME_COORDS = {
            'NEXT_VILLAGE': {'x': 893, 'y': 844},
            'HOME_BUTTON': {'x': 1573, 'y': 809},
            'MIDDLE_OF_SCREEN': {'x': 794, 'y': 439},
            "FILTERS_BUTTON": {'x': 1567, 'y': 768},
            "VILLAGES_IN_YOUR_FACTION": {'x': 154, 'y': 167},
        }

        self.template_service.cache_templates()

    def process_village(self, templates):

        # self.device_service.click_coordinates_and_sleep(
        #     self.GAME_COORDS["FILTERS_BUTTON"])
        # self.device_service.click_coordinates_and_sleep(
        #     self.GAME_COORDS["VILLAGES_IN_YOUR_FACTION"])
        """Process a single village's scouting routine"""
        self.device_service.click_coordinates_and_sleep(
            self.GAME_COORDS['MIDDLE_OF_SCREEN'])
        self.device_service.click_coordinates_and_sleep(
            self.GAME_COORDS['MIDDLE_OF_SCREEN'], 2)

        for template_name in templates:
            if self.device_service.find_and_click_template(template_name):
                logger.info(f"Clicked template: {template_name}")

                self.device_service.sleep(1)
                if self.device_service.find_and_click('SCOUT_BUTTON', 0.52):
                    self.device_service.sleep(1)
                    self.device_service.find_and_click('GO_BUTTON', 0.4)
                    self.device_service.sleep(1)
                    if self.device_service.find_and_click('SCOUT_EXIT_BUTTON', 0.79):
                        self.device_service.sleep(1)
                    self.device_service.sleep(1)
                    return True

            else:
                logger.info(f"Template not found: {template_name}")

        return False

    def run(self):
        """Main loop to run the bot with Ctrl+C handling"""
        try:
            self.device_service.click_coordinates_and_sleep(
                self.GAME_COORDS["FILTERS_BUTTON"])
            self.device_service.click_filter_button("ForagingScouts")
            templates = self.template_service.get_template_bags_names()
            if not templates:
                logger.info(
                    f"No template images found in {self.template_service.TEMPLATES_DIR}")
                return

            logger.info(
                f"Found {len(templates)} templates: {templates}")

            for i in range(self.number_of_villages):
                if i != 0:
                    self.device_service.click_coordinates_and_sleep(
                        self.GAME_COORDS['NEXT_VILLAGE'], 2)
                    self.device_service.click_coordinates_and_sleep(
                        self.GAME_COORDS['HOME_BUTTON'], 2)

                logger.info(f"\nProcessing Village {i + 1}")
                if self.process_village(templates):
                    logger.info(f"Successfully processed Village {i + 1}")
                else:
                    logger.info(f"No action needed for Village {i + 1}")

            self.utils_service.go_to_village_1()

        except KeyboardInterrupt:
            logger.info("\nBot stopped by user (Ctrl+C)")
            logger.info("Cleaning up and exiting...")
            sys.exit(0)
        except Exception as e:
            logger.info(f"\nAn error occurred: {str(e)}")
            raise
