import numpy as np
from pymkbot.features.feature import Feature


class MyHPFeature(Feature):
    def sliceScreenToBar(self, image):
        hp_bar = image[49:64, 14:300].copy()
        mask = ((hp_bar[:, :, 0] > 190) & (hp_bar[:, :, 1] > 190) & (hp_bar[:, :, 2] > 190))
        hp_bar[mask] = [0, 0, 0]
        return hp_bar

    def get_value(self, image, precision=0.1):
        hp_bar = self.sliceScreenToBar(image)
        hp_percentage = 0
        for i in range(1, int(1 / precision)):
            percent = i * precision
            pixel_coord = percent * 285
            if np.max(hp_bar[:, pixel_coord, 2]) > 200:
                hp_percentage += precision * 100
            else:
                break

        return hp_percentage
