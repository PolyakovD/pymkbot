from pathlib import Path

import cv2
import os
import numpy as np
import time

from pymkbot.features.feature import Feature


class MenuFeature(Feature):
    def __init__(self, template_path):
        self._path = Path(template_path)
        self._method = cv2.TM_SQDIFF
        self._templates = {}
        self._load_templates()

    def _load_templates(self):
        for name_image in os.listdir(str(self._path)):
            if os.path.isfile(str(self._path / name_image)):
                name, _ = name_image.split('.')
                img = cv2.imread(str(self._path / name_image))
                self._templates[name] = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    def get_value(self, image):
        time.sleep(0.1)
        for name, template in self._templates.items():
            res = cv2.matchTemplate(image, template, self._method)
            if np.min(res) < 10:
                print(name)
                return name
        return 'not_menu'

    def get_name(self):
        return 'menu_feature'