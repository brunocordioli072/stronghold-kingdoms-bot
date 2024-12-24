import cv2
import os
import glob


class TemplateService:
    def __init__(self, base_path):
        self.base_path = base_path
        self.TEMPLATES_DIR = os.path.join(
            self.base_path, 'stronghold-kingdoms-bot', 'templates', 'bags')
        self.template_cache = {}

    def cache_templates(self):
        """Cache all template images into memory."""
        template_bags_paths = self.get_template_bags_paths()
        for path in template_bags_paths:
            self.template_cache[path] = cv2.imread(path)

        SCOUT_BUTTON_PATH = os.path.join(
            self.base_path, 'stronghold-kingdoms-bot', 'templates', 'general', 'scout_button.png')
        GO_BUTTON_PATH = os.path.join(
            self.base_path, 'stronghold-kingdoms-bot', 'templates', 'general', 'go_button.png')
        SCOUT_EXIT_BUTTON_PATH = os.path.join(
            self.base_path, 'stronghold-kingdoms-bot', 'templates', 'general', 'scout_exit_button.png')

        # Add specific templates to the cache
        self.template_cache['SCOUT_BUTTON'] = cv2.imread(SCOUT_BUTTON_PATH)
        self.template_cache['GO_BUTTON'] = cv2.imread(GO_BUTTON_PATH)
        self.template_cache['SCOUT_EXIT_BUTTON'] = cv2.imread(
            SCOUT_EXIT_BUTTON_PATH)

    def get_template(self, template_path):
        """Get a cached template image by path."""
        return self.template_cache.get(template_path)

    def get_template_bags_paths(self):
        """Get all PNG files from templates directory."""
        template_pattern = os.path.join(self.TEMPLATES_DIR, '*.png')
        return glob.glob(template_pattern)
