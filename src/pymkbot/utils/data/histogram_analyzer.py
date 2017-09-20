import cv2
import numpy as np
import pickle

from scipy.stats.mstats import chisquare


class HistogramAnalyzer:
    def __init__(self, heroes_file):
        with open(heroes_file, 'rb') as file:
            self.heroes_data = pickle.load(file)

    def analyze(self, first_name, second_name, histogram1, histogram2):
        hist1 = histogram1.T[0] / np.sum(histogram1.T[0])
        hist2 = histogram2.T[0] / np.sum(histogram2.T[0])
        model_histogram1 = self.heroes_data[first_name].T[0] / np.sum(self.heroes_data[first_name].T[0])
        model_histogram2 = self.heroes_data[second_name].T[0] / np.sum(self.heroes_data[second_name].T[0])

        xi1_1 = cv2.compareHist(hist1, model_histogram1, method=cv2.HISTCMP_CHISQR)
        xi1_2 = cv2.compareHist(hist1, model_histogram2, method=cv2.HISTCMP_CHISQR)
        xi2_1 = cv2.compareHist(hist2, model_histogram1, method=cv2.HISTCMP_CHISQR)
        xi2_2 = cv2.compareHist(hist2, model_histogram2, method=cv2.HISTCMP_CHISQR)

        a, b = (min(xi1_1, xi2_2), max(xi1_1, xi2_2))
        c, d = (min(xi1_2, xi2_1), max(xi1_2, xi2_1))

        if a < c and b < c:
            return 0, 1
        elif c < a and d < a:
            return 1, 0

        return None

        # p_mat = np.array([[p1_1, p2_1], [p1_2, p2_2]])
        # max_p = (np.argmax(p_mat) // 2, np.argmax(p_mat) % 2)
        # if p_mat[(max_p[0] + 1) % 2, (max_p[1] +1) % 2] > p_mat[(max_p[0] + 1) % 2, max_p[1]]:
        #     if p_mat == 0 or p_mat == 3:
        #         return 0, 1
        #     else:
        #         return 1, 0
        # else:
        #     return None