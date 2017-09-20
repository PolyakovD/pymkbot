import cv2
import numpy as np
from numpy.ma import absolute, nonzero

from pymkbot.features.feature import Feature
from pymkbot.utils.data.histogram_analyzer import HistogramAnalyzer
from pymkbot.utils.data.image_utils import make_kmeans, get_class_mask, get_histogram

FRACTION_MIN = 0.01
FRACTION_MAX = 0.05


class PositionFeature(Feature):
    def get_name(self):
        return "position_feature"

    def __init__(self, name_feature, debug_mode=True):
        self._debug = debug_mode
        self.num_pixels = 0
        self.histogram0 = None
        self.histogram1 = None
        self.centers = None
        self.analyzer = HistogramAnalyzer('character_histogram.pickle')
        self.name_feature = name_feature
        self.images = []

    def get_mask(self):
        diff_image = absolute(cv2.blur(self.images[1], (5, 5)) - cv2.blur(self.images[0], (5, 5)))
        # diff_image = absolute(self.images[1] - self.images[0])
        diff_image = cv2.cvtColor(diff_image, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(diff_image, 127, 255, cv2.THRESH_BINARY)
        return mask

    def get_histogram_centers(self):
        diff_image = absolute(cv2.blur(self.images[1], (5, 5)) - cv2.blur(self.images[0], (5, 5)))
        # diff_image = absolute(self.images[1] - self.images[0])
        diff_image = cv2.cvtColor(diff_image, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(diff_image, 127, 255, cv2.THRESH_BINARY)
        mask_bool = mask.astype(np.bool)
        nonzero_pos = nonzero(mask)
        nonzero_num = len(nonzero_pos[0])
        if FRACTION_MIN * self.num_pixels < nonzero_num < FRACTION_MAX * self.num_pixels:
            data_set = np.vstack(nonzero_pos).T
            mask_label, self.centers = make_kmeans(data_set)
            mask_res = mask_bool.ravel()
            mask_int = np.arange(len(mask_res))

            mask0 = get_class_mask(mask_res, mask_label, mask_int, mask_bool, 0)
            mask1 = get_class_mask(mask_res, mask_label, mask_int, mask_bool, 1)

            self.histogram0 = get_histogram(self.images[1], mask0)
            self.histogram1 = get_histogram(self.images[1], mask1)

            if self._debug:
                self._debug_output(mask, mask0, mask1)

    def _debug_output(self, mask, mask0, mask1):
        red = (mask0 * 255).astype(np.uint8)
        green = (mask1 * 255).astype(np.uint8)
        diff_image = cv2.merge((red, green, mask))
        for y, x in self.centers:
            x = int(x)
            y = int(y)
            cv2.rectangle(diff_image, (x - 10, y - 10), (x + 10, y + 10), (255, 0, 0), 2)

        cv2.imshow("windows2", diff_image)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    def get_value(self, image):
        first_name, second_name = self.name_feature.get_value(image)
        if first_name is None or second_name is None:
            return None
        if self.num_pixels == 0:
            self.num_pixels = np.prod(image.shape)

        self.images.append(image)
        if len(self.images) == 1:
            return None

        self.get_histogram_centers()
        self.images = []

        if self.histogram0 is None or self.histogram1 is None:
            return None
        new_order = self.analyzer.analyze(first_name, second_name, self.histogram0, self.histogram1)
        if new_order is None:
            return None
        if new_order[0] == 0:
            return self.centers[::-1], self.centers[::-1]
        else:
            return self.centers[::-1], self.centers[::-1]
