import pymkbot.keyboard.directkeys as keys


class Strategy:
    def __init__(self, player):
        self._key_bindings = keys.keyboard[player]
        self._player = player
        self._released = True

    def do_action(self):
        pass

    def release(self):
        if not self._released:
            self._release()

    def _release(self):
        raise NotImplementedError

