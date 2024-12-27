from services.device_service import DeviceService
from services.config_service import ConfigService


class UtilsService:
    """Provides utility functions"""

    def __init__(self, device_service: DeviceService):
        """Sets up the service with device controls and screen coordinates"""
        self.device_service = device_service
        self.config_service = ConfigService()
        config = self.config_service.load_config()
        self.village_1_name = config['village_1_name']

        self.VILLAGE_NUMBER_TOP_LEFT = {'x': 670, 'y': 780}
        self.VILLAGE_NUMBER_BOTTOM_RIGHT = {'x': 913, 'y': 820}
        self.NEXT_VILLAGE = {'x': 970, 'y': 809}
        self.HOME_BUTTON = {'x': 1548, 'y': 761}

    def go_to_village_1(self):
        """Navigates to village 1 by repeatedly clicking next until found"""
        village_name = self.device_service.get_text_from_coords(
            self.VILLAGE_NUMBER_TOP_LEFT, self.VILLAGE_NUMBER_BOTTOM_RIGHT)

        print(
            f"Current village name: {village_name}, Target village: {self.village_1_name}")

        if village_name and village_name == self.village_1_name:
            print("Found target village, clicking home button")
            self.device_service.click_coordinates_and_sleep(
                self.HOME_BUTTON, 2)
        else:
            print("Not at target village, clicking next")
            self.device_service.click_coordinates_and_sleep(
                self.NEXT_VILLAGE, 2)
            self.go_to_village_1()
