from datetime import datetime
import time

import pymkbot.keyboard.directkeys as keys


class Strategy:
    def __init__(self):
        self._begin_time = datetime.now()
        self._strat_len = 5.0
        self._current_action = 'attack'

    def _attack(self):
        if self._current_action == 'defence':
            self._stop_defence()
        keys.release_key(keys.HIGH_PUNCH)
        time.sleep(0.05)
        keys.press_key(keys.HIGH_PUNCH)
        keys.press_key(keys.RIGHT)
        #print("u")
        #time.sleep(0.1)
        self._current_action = 'attack'

    def _defence(self):
        if self._current_action == 'attack':
            self._stop_attack()
        keys.press_key(keys.LEFT)
        keys.press_key(keys.UP)
        self._current_action = 'defence'

    def _stop_attack(self):
        keys.release_key(keys.HIGH_PUNCH)
        keys.release_key(keys.RIGHT)
        time.sleep(0.1)

    def _stop_defence(self):
        keys.release_key(keys.LEFT)
        keys.release_key(keys.UP)
        time.sleep(0.1)

    def get_action(self):
        t = datetime.now()
        delta = t - self._begin_time
        t_beg = (delta.seconds + delta.microseconds / 1E6) % self._strat_len
        if t_beg > (self._strat_len * 0.8):
            self._defence()
        else:
            self._attack()



