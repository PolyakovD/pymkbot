import time

import pymkbot.keyboard.directkeys as keys


class Strategy:
    def __init__(self, player, keybd_switch):
        self._key_bindings = keys.keyboard[player]
        self._player = player
        self._released = True
        self._keybd_switch = keybd_switch

    def do_action(self):
        pass

    def release(self):
        if not self._released:
            self._release()

    def _release(self):
        raise NotImplementedError

    def run_strategy(self, switch):
        while True:
            if self._keybd_switch.get_key_state(switch):
                self.do_action()
            else:
                self.release()
            time.sleep(0.05)
