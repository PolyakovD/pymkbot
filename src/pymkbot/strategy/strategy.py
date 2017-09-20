class Strategy:
    def __init__(self, key_bindings):
        self._key_bindings = key_bindings
        self._released = True

    def do_action(self):
        pass

    def release(self):
        if not self._released:
            self._release()

    def _release(self):
        raise NotImplementedError

