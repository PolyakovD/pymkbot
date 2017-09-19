import datetime

from pymkbot.keyboard.directkeys import W, A, S, D, press_key, release_key


class Strategy:
    def __init__(self):
        self._begin_time = datetime.now()
        self._strat_len = 2.0
        self._current_action = 'attack'

    def _attack(self):
        if self._current_action == 'defence':
            self._stop_defence()
        #release_key(U)
        #press_key(U)
        press_key(D)

    def _defence(self):
        if self._current_action == 'attack':
            self._stop_attack()
        press_key(A)
        press_key(W)

    def _stop_attack(self):
        #release_key(U)
        release_key(D)

    def _stop_defence(self):
        release_key(A)
        release_key(W)

    def get_action(self):
        t = datetime.now()
        delta = t - self._begin_time
        t_beg = (delta.seconds + delta.microseconds / 1E6) % self._strat_len
        if t_beg > (self._strat_len / 2.0):
            self._defence()
        else:
            self._attack()



