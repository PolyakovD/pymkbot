import cv2
import numpy
from numpy.core.multiarray import unravel_index
from numpy.ma import absolute, nonzero, dstack, empty, zeros
from sklearn.cluster import KMeans

from pymkbot.features.Feature import Feature

LIMIT_INFERIOR = 3000
LIMIT_SUPERIOR = 70000


class MyPositionFeature(Feature):
    def __init__(self):
        self.base_image = None
        self.have_base = False

    def get_value(self, image):
        if self.have_base:
            diff_image = absolute(cv2.blur(image, (5, 5)) - self.base_image)
            diff_image = cv2.cvtColor(diff_image, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(diff_image, 127, 255, cv2.THRESH_BINARY)
            nonzero_pos = nonzero(mask)
            nonzero_num = len(nonzero_pos[0])
            if LIMIT_INFERIOR < nonzero_num < LIMIT_SUPERIOR:
                data_set = empty((nonzero_pos[0].shape[0], 2))
                data_set[:, 0] = nonzero_pos[0]
                data_set[:, 1] = nonzero_pos[1]
                kmeans_res = KMeans(n_clusters=2, random_state=0).fit(data_set)
                # first_class_pos = data_set[kmeans_res.labels_ == 0, :]
                # first_class_mask = zeros(diff_image.shape, dtype=numpy.int)
                # first_class_mask[first_class_pos[:, 0], first_class_pos[:, 1]] = 255
                #
                # second_class_pos = data_set[kmeans_res.labels_ == 1, :]
                # second_class_mask = zeros(diff_image.shape, dtype=numpy.int)
                # second_class_mask[second_class_pos[:, 0], second_class_pos[:, 1]] = 255

                # second_mask = np.zeros(diff_image.shape, np.uint8)
                # mask[100:300, 100:400] = 255
                # masked_img = cv2.bitwise_and(img, img, mask=mask)
                # print((data_set.shape, first_class_pos.shape, second_class_pos.shape))

                diff_image = cv2.merge((mask, mask, mask))
                for y, x in kmeans_res.cluster_centers_:
                    x = int(x)
                    y = int(y)
                    cv2.rectangle(diff_image, (x - 10, y - 10), (x + 10, y + 10), (255, 0, 0), 2)

                cv2.imshow("windows2", diff_image)

            self.base_image = cv2.blur(image, (5, 5))
        else:
            self.base_image = cv2.blur(image, (5, 5))
            self.have_base = True
            # processed_image = image[240:430, :]
            # red_image = processed_image[:, :, 0]
            # processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
            # blur = cv2.blur(processed_image, (80, 80))
            # x, y = unravel_index(red_image.argmax(), red_image.shape)
            # cv2.rectangle(red_image, (x - 1, y - 1), (x + 1, y + 1), (255, 0, 0), 2)
            # cv2.imshow("windows2", red_image)
