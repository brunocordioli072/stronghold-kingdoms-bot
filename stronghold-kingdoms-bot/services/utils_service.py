from services.device_service import DeviceService


class UtilsService:
    def __init__(self, device_service: DeviceService):
        self.device_service = device_service

        self.VILLAGE_NUMBER_TOP_LEFT = {'x': 840, 'y': 782}
        self.VILLAGE_NUMBER_BOTTOM_RIGHT = {'x': 893, 'y': 816}
        self.NEXT_VILLAGE = {'x': 970, 'y': 809}
        self.HOME_BUTTON = {'x': 1548, 'y': 761}

    def go_to_village_1(self):
        number = self.device_service.get_numbers_from_coords(
            self.VILLAGE_NUMBER_TOP_LEFT, self.VILLAGE_NUMBER_BOTTOM_RIGHT)
        if number and int(number) != 1:
            self.device_service.click_coordinates_and_sleep(
                self.NEXT_VILLAGE, 2)
            self.go_to_village_1()
        else:
            self.device_service.click_coordinates_and_sleep(
                self.HOME_BUTTON, 2)
