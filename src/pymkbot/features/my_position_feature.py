import cv2
import numpy as np
from numpy.ma import absolute, nonzero
from pymkbot.features.feature import Feature
from pymkbot.utils.data.image_utils import make_kmeans, get_class_mask, get_histogram

FRACTION_MIN = 0.01
FRACTION_MAX = 0.1


class MyPositionFeature(Feature):
    def __init__(self, debug_mode=True):
        self.base_image = None
        self._debug = debug_mode
        self.have_base = False
        self.num_pixels = 0
        self.histogram0 = None
        self.histogram1 = None
        self.centers = None

    def get_mask(self, image):
        differential_image = absolute(cv2.blur(image, (5, 5)) - self.base_image)
        differential_image = cv2.cvtColor(differential_image, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(differential_image, 127, 255, cv2.THRESH_BINARY)
        return mask

    def get_histogram_centers(self, image):
        diff_image = absolute(cv2.blur(image, (5, 5)) - self.base_image)
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

            self.histogram0 = get_histogram(image, mask0)
            self.histogram1 = get_histogram(image, mask1)
            ###
            red = (mask0 * 255).astype(np.uint8)
            green = (mask1 * 255).astype(np.uint8)
            diff_image = cv2.merge((red, green, mask))

            if self._debug:
                self._debug_output(diff_image)

    def _debug_output(self, diff_image):
        for y, x in self.centers:
            x = int(x)
            y = int(y)
            cv2.rectangle(diff_image, (x - 10, y - 10), (x + 10, y + 10), (255, 0, 0), 2)

        cv2.imshow("windows2", diff_image)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    def get_value(self, image):
        if self.have_base:
            self.get_histogram_centers(image)
            self.base_image = cv2.blur(image, (5, 5))
            return self.centers
        else:
            self.base_image = cv2.blur(image, (5, 5))
            self.have_base = True
            self.num_pixels = np.prod(image.shape)
            return None
