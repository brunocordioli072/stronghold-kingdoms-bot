from stronghold_kingdoms_bot.services.device_service import DeviceService
from stronghold_kingdoms_bot.services.config_service import ConfigService
from loguru import logger


class UtilsService:
    """Provides utility functions"""

    def __init__(self, device_service: DeviceService):
        """Sets up the service with device controls and screen coordinates"""
        self.device_service = device_service
        self.config_service = ConfigService()
        config = self.config_service.load_config()
        self.village_1_name = config['village_1_name']

        self.VILLAGE_NUMBER_TOP_LEFT = {'x': 730, 'y': 825}
        self.VILLAGE_NUMBER_BOTTOM_RIGHT = {'x': 859, 'y': 850}
        self.NEXT_VILLAGE = {'x': 892, 'y': 852}
        self.HOME_BUTTON = {'x': 1573, 'y': 809}

    def go_to_village_1(self):
        """Navigates to village 1 by repeatedly clicking next until found"""
        village_name = self.device_service.get_text_from_coords(
            self.VILLAGE_NUMBER_TOP_LEFT, self.VILLAGE_NUMBER_BOTTOM_RIGHT)

        logger.info(
            f"Current village name: {village_name}, Target village: {self.village_1_name}")

        if village_name and village_name == self.village_1_name:
            logger.info("Found target village, clicking home button")
            self.device_service.click_coordinates_and_sleep(
                self.HOME_BUTTON, 2)
        else:
            logger.info("Not at target village, clicking next")
            self.device_service.click_coordinates_and_sleep(
                self.NEXT_VILLAGE, 2)
            self.go_to_village_1()
