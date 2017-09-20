from datetime import datetime
from pymkbot.strategy.strategy import Strategy
import time

import pymkbot.keyboard.directkeys as keys


class LuKengNaiveStrategy(Strategy):
    def __init__(self, player):
        super().__init__(player)
        self._begin_time = datetime.now()
        self._strat_len = 2.0
        self._current_action = 'attack'

    def _attack(self):
        keys.press_key(self._key_bindings['RIGHT'])
        time.sleep(0.05)
        keys.release_key(self._key_bindings['RIGHT'])
        time.sleep(0.05)
        keys.press_key(self._key_bindings['RIGHT'])
        time.sleep(0.05)
        keys.release_key(self._key_bindings['RIGHT'])
        time.sleep(0.05)
        keys.release_key(self._key_bindings['HIGH_KICK'])
        time.sleep(0.05)
        keys.press_key(self._key_bindings['HIGH_KICK'])
        self._current_action = 'attack'

    def _defence(self):
        keys.press_key(self._key_bindings['LEFT'])
        time.sleep(0.05)
        keys.release_key(self._key_bindings['LEFT'])
        time.sleep(0.05)
        keys.press_key(self._key_bindings['LEFT'])
        time.sleep(0.05)
        keys.release_key(self._key_bindings['LEFT'])
        time.sleep(0.05)
        keys.release_key(self._key_bindings['HIGH_KICK'])
        time.sleep(0.05)
        keys.press_key(self._key_bindings['HIGH_KICK'])
        self._current_action = 'defence'

    def _stop_attack(self):
        keys.release_key(self._key_bindings['HIGH_PUNCH'])
        keys.release_key(self._key_bindings['RIGHT'])
        time.sleep(0.1)

    def _stop_defence(self):
        keys.release_key(self._key_bindings['LEFT'])
        keys.release_key(self._key_bindings['UP'])
        time.sleep(0.1)

    def _release(self):
        for action in ['LEFT', 'RIGHT', 'HIGH_KICK']:
            keys.release_key(self._key_bindings[action])

    def do_action(self):
        t = datetime.now()
        delta = t - self._begin_time
        t_beg = (delta.seconds + delta.microseconds / 1E6) % self._strat_len
        if t_beg > (self._strat_len * 0.5):
            self._defence()
        else:
            self._attack()



