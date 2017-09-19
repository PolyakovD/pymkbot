VK_CAPITAL = 0x14
VK_SCROLL = 0x91


class KeyStateGetter:
    def __init__(self):
        import ctypes
        self._hllDll = ctypes.WinDLL("User32.dll")

    def get_key_state(self, key=VK_CAPITAL):
        return self._hllDll.GetKeyState(key) % 2