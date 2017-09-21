import time

import pymkbot.keyboard.directkeys as keys


class Strategy:
    def __init__(self, player, keybd_switch, *, key_switch=None):
        self._key_bindings = keys.keyboard[player]
        self._player = player
        self._released = True
        self._keybd_switch = keybd_switch
        self._key_switch = key_switch

    def release(self):
        if not self._released:
            self._release()

    def _release(self):
        raise NotImplementedError

    def prepare(self):
        pass

    def stop(self):
        raise NotImplementedError

    def resume(self):
        raise NotImplementedError
