from pathlib import Path

import cv2
import numpy as np
import os

import time

ROI_0 = np.array([9, 27, 88, 35])
ROI_1 = np.array([232, 27, 311, 35])

class NameParser:
    def __init__(self, path):
        self._path = Path(path)
        self._roi0 = ROI_0
        self._roi1 = ROI_1
        self._pos0 = np.array([9, 36])
        self._offset = np.array([0, 0])
        self._current_image = None
        self._names = [{}, {}]
        self._save_idx = 0
        self._load_images()

    def _load_images(self):
        for name_image in os.listdir(str(self._path)):
            name, side, _ = name_image.split('.')
            img = cv2.imread(str(self._path / name_image))
            letter_mask = (img[:, :, 0] < 255) | (img[:, :, 1] > 0)
            self._names[int(side)][name] = (img, letter_mask)

    def _calibrate(self):
        if self._current_image is None:
            return
        img = self._current_image.copy()

        col = img[:, 25, :]
        mask_green_v = (col[:, 1] > 250) & (col[:, 0] < 150) & (col[:, 2] < 100)
        if mask_green_v.any():
            self._offset[1] = np.min(np.arange(len(mask_green_v))[mask_green_v]) - self._pos0[1]

        row = img[self._pos0[1] + self._offset[1], :, :]
        mask_green_h = (row[:, 1] > 250) & (row[:, 0] < 150) & (row[:, 2] < 100)
        if mask_green_h.any():
            self._offset[0] = np.min(np.arange(len(mask_green_h))[mask_green_h]) - self._pos0[0]


        self._roi0 = ROI_0 + np.hstack([self._offset, self._offset])
        self._roi1 = ROI_1 + np.hstack([self._offset, self._offset])
        self._roi1[2] = min(self._roi1[2], 320)

        print('CALIBRATED, offset = ' + str(self._offset))

    def _get_names(self, img):
        imgs_cur = [img[self._roi0[1]:self._roi0[3], self._roi0[0]:self._roi0[2]],
                    img[self._roi1[1]:self._roi1[3], self._roi1[0]:self._roi1[2]]]
        result = [None, None]
        for side in [0, 1]:
            for name, (image, mask) in self._names[side].items():
                if np.median(np.abs(image[mask] - imgs_cur[side][mask])) == 0:
                    result[side] = name
        return result

    def process_image(self, img):
        self._current_image = img.copy()
        return self._get_names(img)

    def on_save_image_hotkey(self):
        self.save_image(self._current_image)

    def save_image(self, img):
        img_0 = cv2.cvtColor(img[self._roi0[1]:self._roi0[3], self._roi0[0]:self._roi0[2]], cv2.COLOR_RGB2BGR)
        img_1 = cv2.cvtColor(img[self._roi1[1]:self._roi1[3], self._roi1[0]:self._roi1[2]], cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(self._path / (str(self._save_idx) + '.0.png')), img_0)
        cv2.imwrite(str(self._path / (str(self._save_idx) + '.1.png')), img_1)
        self._save_idx += 1
        print('SAVED')

