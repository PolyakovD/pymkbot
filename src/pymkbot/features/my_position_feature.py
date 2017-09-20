import cv2
import numpy as np
from numpy.ma import absolute, nonzero
from sklearn.cluster import KMeans

from pymkbot.features.Feature import Feature

FRAC_MIN = 0.01
FRAC_MAX = 0.1


def make_kmeans(data_set):
    kmeans_res = KMeans(n_clusters=2, random_state=0).fit(data_set)
    return kmeans_res.labels_, kmeans_res.cluster_centers_


def get_class_mask(mask_res, mask_label, mask_int, mask_bool, class_num):
    class_mask_int = mask_int[mask_res][mask_label == class_num]
    class_mask = np.zeros_like(mask_res)
    class_mask[class_mask_int] = 1
    return class_mask.reshape(mask_bool.shape)


class MyPositionFeature(Feature):
    def __init__(self):
        self.base_image = None
        self.have_base = False
        self.num_pixels = 0

    def get_mask(self, image):
        differential_image = absolute(cv2.blur(image, (5, 5)) - self.base_image)
        differential_image = cv2.cvtColor(differential_image, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(differential_image, 127, 255, cv2.THRESH_BINARY)
        return mask

    def get_value(self, image):
        if self.have_base:
            diff_image = absolute(cv2.blur(image, (5, 5)) - self.base_image)
            diff_image = cv2.cvtColor(diff_image, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(diff_image, 127, 255, cv2.THRESH_BINARY)
            mask_bool = mask.astype(np.bool)
            nonzero_pos = nonzero(mask)
            nonzero_num = len(nonzero_pos[0])
            if FRAC_MIN * self.num_pixels < nonzero_num < FRAC_MAX * self.num_pixels:
                data_set = np.vstack(nonzero_pos).T
                mask_label, centers = make_kmeans(data_set)
                mask_res = mask_bool.ravel()
                mask_int = np.arange(len(mask_res))

                mask0 = get_class_mask(mask_res, mask_label, mask_int, mask_bool, 0)
                # mask0_int = mask_int[mask_res][mask_label == 0]
                # mask0 = np.zeros_like(mask_res)
                # mask0[mask0_int] = 1
                # mask0 = mask0.reshape(mask_bool.shape)

                mask1 = get_class_mask(mask_res, mask_label, mask_int, mask_bool, 1)
                # mask1_int = mask_int[mask_res][mask_label == 1]
                # mask1 = np.zeros_like(mask_res)
                # mask1[mask1_int] = 1
                # mask1 = mask1.reshape(mask_bool.shape)

                red = (mask0 * 255).astype(np.uint8)
                green = (mask1 * 255).astype(np.uint8)
                diff_image = cv2.merge((red, green, mask))
                for y, x in centers:
                    x = int(x)
                    y = int(y)
                    cv2.rectangle(diff_image, (x - 10, y - 10), (x + 10, y + 10), (255, 0, 0), 2)

                cv2.imshow("windows2", diff_image)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()

            self.base_image = cv2.blur(image, (5, 5))
        else:
            self.base_image = cv2.blur(image, (5, 5))
            self.have_base = True
            self.num_pixels = np.prod(image.shape)
            # processed_image = image[240:430, :]
            # red_image = processed_image[:, :, 0]
            # processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
            # blur = cv2.blur(processed_image, (80, 80))
            # x, y = unravel_index(red_image.argmax(), red_image.shape)
            # cv2.rectangle(red_image, (x - 1, y - 1), (x + 1, y + 1), (255, 0, 0), 2)
            # cv2.imshow("windows2", red_image)
