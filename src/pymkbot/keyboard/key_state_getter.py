import time

from pymkbot.utils.async_executor import AsyncExecutor

CAPS_LOCK = 0x14
SCROLL_LOCK = 0x91


class KeyStateGetter:
    def __init__(self):
        import ctypes
        self._hllDll = ctypes.WinDLL("User32.dll")

    def get_key_state(self, key=CAPS_LOCK):
        return self._hllDll.GetKeyState(key) % 2


class KeyPressCallback:
    def __init__(self):
        import ctypes
        self._hllDll = ctypes.WinDLL("User32.dll")
        self._callbacks = {}
        self._executor = AsyncExecutor()
        self._pressed = set()
        self._executor.call_soon_threadsafe(self.check_states_forever)

    def add_key_callback(self, key, callback):
        self._callbacks[key] = callback

    def check_states_forever(self):
        while True:
            for key in self._callbacks.keys():
                pressed = self._hllDll.GetKeyState(key) & 0x8000
                if pressed:
                    if key not in self._pressed:
                        self._callbacks[key]()
                        self._pressed.add(key)
                elif key in self._pressed:
                    self._pressed.remove(key)
            time.sleep(0.05)
