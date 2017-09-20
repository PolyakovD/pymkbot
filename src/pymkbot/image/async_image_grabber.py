import numpy as np
import cv2

from pymkbot.utils.async_executor import AsyncExecutor

import win32gui, win32ui, win32con, win32api


class AsyncImageGrabber:
    def __init__(self, region=None, debug_image_size=None):
        self._hwin = win32gui.GetDesktopWindow()

        if region:
            left, top, x2, y2 = region
            self._offset = (left, top)
            self._size = (x2 - left + 1, y2 - top + 1)
        else:
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            self._size = (width, height)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
            self._offset = (left, top)

        self._executor = AsyncExecutor()
        self._callback = None
        if debug_image_size:
            self._debug_image_size = debug_image_size
        else:
            self._debug_image_size = self._size
        self._current_img = None
        self._show_image = True

    @property
    def image(self):
        return self._current_img

    def _debug_show_image_scaled(self):
        img_scaled = cv2.resize(self._current_img, dsize=self._debug_image_size, interpolation=cv2.INTER_NEAREST)
        cv2.imshow('window', cv2.cvtColor(img_scaled, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    def _record_screen_forever(self):
        width, height = self._size
        while True:
            self._hwindc = win32gui.GetWindowDC(self._hwin)
            srcdc = win32ui.CreateDCFromHandle(self._hwindc)
            memdc = srcdc.CreateCompatibleDC()
            bmp = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(srcdc, width, height)
            memdc.SelectObject(bmp)
            memdc.BitBlt((0, 0), (width, height), srcdc, self._offset, win32con.SRCCOPY)

            signedIntsArray = bmp.GetBitmapBits(True)
            img = np.fromstring(signedIntsArray, dtype='uint8')
            img.shape = (height, width, 4)

            srcdc.DeleteDC()
            memdc.DeleteDC()
            win32gui.ReleaseDC(self._hwin, self._hwindc)
            win32gui.DeleteObject(bmp.GetHandle())

            self._current_img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

            if self._show_image:
                self._debug_show_image_scaled()
            if self._callback:
                self._callback()

    def begin_recording(self):
        self._executor.call_soon_threadsafe(self._record_screen_forever)

    def set_callback(self, callback):
        self._callback = callback
