import datetime

import pymkbot.keyboard.directkeys as keys


class Strategy:
    def __init__(self):
        self._begin_time = datetime.now()
        self._strat_len = 2.0
        self._current_action = 'attack'

    def _attack(self):
        if self._current_action == 'defence':
            self._stop_defence()
        keys.release_key(keys.HIGH_PUNCH)
        keys.press_key(keys.HIGH_PUNCH)
        keys.press_key(keys.RIGHT)

    def _defence(self):
        if self._current_action == 'attack':
            self._stop_attack()
        keys.press_key(keys.LEFT)
        keys.press_key(keys.UP)

    def _stop_attack(self):
        keys.release_key(keys.HIGH_PUNCH)
        keys.release_key(keys.RIGHT)

    def _stop_defence(self):
        keys.release_key(keys.LEFT)
        keys.release_key(keys.UP)

    def get_action(self):
        t = datetime.now()
        delta = t - self._begin_time
        t_beg = (delta.seconds + delta.microseconds / 1E6) % self._strat_len
        if t_beg > (self._strat_len / 2.0):
            self._defence()
        else:
            self._attack()



