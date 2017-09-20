import cv2
import numpy as np
from sklearn.cluster import KMeans


def make_kmeans(data_set):
    kmeans_res = KMeans(n_clusters=2, random_state=0).fit(data_set)
    return kmeans_res.labels_, kmeans_res.cluster_centers_


def get_class_mask(mask_res, mask_label, mask_int, mask_bool, class_label):
    class_mask_int = mask_int[mask_res][mask_label == class_label]
    class_mask = np.zeros_like(mask_res, dtype=np.uint8)
    class_mask[class_mask_int] = 1
    return class_mask.reshape(mask_bool.shape)


def get_histogram(image, mask):
    hist_r = cv2.calcHist([image], [0], mask, [256], [0, 256])
    hist_g = cv2.calcHist([image], [1], mask, [256], [0, 256])
    hist_b = cv2.calcHist([image], [2], mask, [256], [0, 256])

    return np.concatenate((hist_r, hist_g, hist_b), axis=0)
