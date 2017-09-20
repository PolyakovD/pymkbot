import numpy as np

from pymkbot.features.feature import Feature


class HPFeature(Feature):
    def __init__(self, player):
        self.player = player
        self.shape = [0, 0]
        self.bar_coords = [{}, {}]

    def updateShape(self, image):
        if self.shape != image.shape:
            self.shape = image.shape
            y, x = image.shape
            self.bar_coords = [
                {
                    'y1': int(50 / 480 * y),
                    'y2': int(65 / 480 * y),
                    'x1': int(15 / 640 * x),
                    'x2': int(300 / 640 * x)
                },
                {
                    'y1': int(50 / 480 * y),
                    'y2': int(65 / 480 * y),
                    'x2': int((640 - 15 / 640) * x),
                    'x1': int((640 - 300 / 640) * x)
                }
            ]

    def sliceScreenToBar(self, image, player):
        self.updateShape(image)
        coord = self.bar_coords[player]
        hp_bar = image[coord['y1'], coord['y2'], coord['x1']:coord['x2']].copy()
        mask = ((hp_bar[:, :, 0] > 190) & (hp_bar[:, :, 1] > 190) & (hp_bar[:, :, 2] > 190))
        hp_bar[mask] = [0, 0, 0]

        if player == 1:
            hp_bar = hp_bar[:, ::-1]

        return hp_bar

    def get_value(self, image, player=0, precision=0.1):
        hp_bar = self.sliceScreenToBar(image, player)
        hp_percentage = 0
        for i in range(1, int(1 / precision)):
            percent = i * precision
            pixel_coord = percent * 285
            if np.max(hp_bar[:, pixel_coord, 2]) > 200:
                hp_percentage += precision * 100
            else:
                break

        return hp_percentage
