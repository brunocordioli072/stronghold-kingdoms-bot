import os
import sys
from services.config_service import ConfigService
from services.template_service import TemplateService
from services.device_service import DeviceService
from services.utils_service import UtilsService


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
            'NEXT_VILLAGE': {'x': 970, 'y': 809},
            'HOME_BUTTON': {'x': 1548, 'y': 761},
            'MIDDLE_OF_SCREEN': {'x': 794, 'y': 439},
        }

        self.template_service.cache_templates()

    def process_village(self, templates):
        """Process a single village's scouting routine"""
        self.device_service.click_coordinates_and_sleep(
            self.GAME_COORDS['MIDDLE_OF_SCREEN'])
        self.device_service.click_coordinates_and_sleep(
            self.GAME_COORDS['MIDDLE_OF_SCREEN'])

        for template_path in templates:
            if self.device_service.find_and_click(template_path):
                print(f"Clicked template: {os.path.basename(template_path)}")

                self.device_service.sleep(1)
                if self.device_service.find_and_click('SCOUT_BUTTON'):
                    self.device_service.sleep(1)
                    self.device_service.find_and_click('GO_BUTTON')
                    self.device_service.sleep(1)
                    if self.device_service.find_and_click('SCOUT_EXIT_BUTTON'):
                        self.device_service.sleep(2)
                    return True

            else:
                print(f"Template not found: {os.path.basename(template_path)}")

        return False

    def run(self):
        """Main loop to run the bot with Ctrl+C handling"""
        try:
            templates = self.template_service.get_template_bags_paths()
            if not templates:
                print(
                    f"No template images found in {self.template_service.TEMPLATES_DIR}")
                return

            print(
                f"Found {len(templates)} templates: {[os.path.basename(t) for t in templates]}")

            for i in range(self.number_of_villages):
                if i != 0:
                    self.device_service.click_coordinates_and_sleep(
                        self.GAME_COORDS['NEXT_VILLAGE'], 2)
                    self.device_service.click_coordinates_and_sleep(
                        self.GAME_COORDS['HOME_BUTTON'], 2)

                print(f"\nProcessing Village {i + 1}")
                if self.process_village(templates):
                    print(f"Successfully processed Village {i + 1}")
                else:
                    print(f"No action needed for Village {i + 1}")

                self.device_service.sleep(2)

            self.utils_service.go_to_village_1()

        except KeyboardInterrupt:
            print("\nBot stopped by user (Ctrl+C)")
            print("Cleaning up and exiting...")
            sys.exit(0)
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            raise
