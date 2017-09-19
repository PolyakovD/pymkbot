import numpy as np
from PIL import ImageGrab
import cv2

from pymkbot.utils.async_executor import AsyncExecutor


class AsyncImageGrabber:
    def __init__(self):
        self._executor = AsyncExecutor()
        self._callback = None
        self._in_size = [320, 240]
        self._out_size = [680, 480]
        self._current_img = None

    def _debug_show_image_scaled(self):
        img_scaled = cv2.resize(self._current_img, dsize=self._out_size, interpolation=cv2.INTER_NEAREST)
        cv2.imshow('window', cv2.cvtColor(img_scaled, cv2.COLOR_BGR2RGB))

    def _record_screen_forever(self):
        while True:
            self._current_img = np.array(ImageGrab.grab(bbox=(0, 30, 320, 270)))
            self._debug_show_image_scaled()
            if self._callback:
                self._callback()

    def begin_recording(self):
        self._executor.call_soon_threadsafe(self._record_screen_forever)

    def set_callback(self, callback):
        self._callback = callback