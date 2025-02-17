import cv2
import os
import glob


class TemplateService:
    def __init__(self, base_path):
        self.base_path = base_path
        self.TEMPLATES_DIR = os.path.join(
            self.base_path, 'stronghold_kingdoms_bot', 'templates', 'bags')
        self.template_cache = []

    def cache_templates(self):
        """Cache all template images into memory."""

        # General templates
        general_templates = [
            {"name": "SCOUT_BUTTON", "filename": "scout_button.png"},
            {"name": "GO_BUTTON", "filename": "go_button.png"},
            {"name": "SCOUT_EXIT_BUTTON", "filename": "scout_exit_button.png"}
        ]
        self.add_templates("general", general_templates, threshold=0.7)

        # Bag templates
        bag_templates = [
            {"name": "ale", "filename": "ale.png", "threshold": 0.7},
            {"name": "apple", "filename": "apple.png", "threshold": 0.7},
            {"name": "bag", "filename": "bag.png", "threshold": 0.7},
            {"name": "bread", "filename": "bread.png", "threshold": 0.7},
            {"name": "cheese", "filename": "cheese.png", "threshold": 0.7},
            {"name": "clothes", "filename": "clothes.png", "threshold": 0.7},
            {"name": "fish", "filename": "fish.png", "threshold": 0.7},
            {"name": "furniture", "filename": "furniture.png", "threshold": 0.7},
            {"name": "meat", "filename": "meat.png", "threshold": 0.7},
            {"name": "metal", "filename": "metal.png", "threshold": 0.7},
            {"name": "metalware", "filename": "metalware.png", "threshold": 0.7},
            {"name": "pitch", "filename": "pitch.png", "threshold": 0.7},
            {"name": "salt", "filename": "salt.png", "threshold": 0.7},
            {"name": "silk", "filename": "silk.png", "threshold": 0.7},
            {"name": "spice", "filename": "spice.png", "threshold": 0.7},
            {"name": "stone", "filename": "stone.png", "threshold": 0.7},
            {"name": "veggies", "filename": "veggies.png", "threshold": 0.7},
            {"name": "venison", "filename": "venison.png", "threshold": 0.7},
            {"name": "wine", "filename": "wine.png", "threshold": 0.7},
            {"name": "wood", "filename": "wood.png", "threshold": 0.7}
        ]
        self.add_templates("bags", bag_templates)

        self.filter_buttons = {
            1: {'top_left': {'x': 46, 'y': 58}, 'right_bottom': {'x': 299, 'y': 86}},
            2: {'top_left': {'x': 46, 'y': 108}, 'right_bottom': {'x': 299, 'y': 133}},
            3: {'top_left': {'x': 46, 'y': 154}, 'right_bottom': {'x': 299, 'y': 180}},
            4: {'top_left': {'x': 46, 'y': 203}, 'right_bottom': {'x': 299, 'y': 226}},
            5: {'top_left': {'x': 46, 'y': 249}, 'right_bottom': {'x': 299, 'y': 276}},
            6: {'top_left': {'x': 46, 'y': 295}, 'right_bottom': {'x': 299, 'y': 327}},
            7: {'top_left': {'x': 46, 'y': 344}, 'right_bottom': {'x': 299, 'y': 373}},
        }

    def add_templates(self, folder, templates, threshold=0.7):
        """
        Adds templates to the template cache.

        :param folder: The subfolder under 'stronghold-kingdoms-bot/templates' where the images are located.
        :param templates: A list of dictionaries containing template details (name and filename).
        :param threshold: Default threshold for template matching.
        """
        for template in templates:
            path = os.path.join(self.base_path, 'stronghold_kingdoms_bot',
                                'templates', folder, template["filename"])
            template_entry = {
                "name": template["name"],
                "path": path,
                "img": cv2.imread(path),
                "threshold": template.get("threshold", threshold)
            }
            self.template_cache.append(template_entry)

    def get_template(self, template_name):
        """Get a cached template image by path."""
        for template in self.template_cache:
            if template["name"] == template_name:
                return template

    def get_template_bags_names(self):
        """Get names of all PNG files from templates directory."""
        template_pattern = os.path.join(self.TEMPLATES_DIR, '*.png')
        # Get full paths first
        paths = glob.glob(template_pattern)
        # Extract just the filenames without extension
        return [os.path.splitext(os.path.basename(path))[0] for path in paths]
