from datetime import datetime
from pymkbot.strategy.strategy import Strategy
import time
import random

import pymkbot.keyboard.directkeys as keys


moves = ['LEFT', 'RIGHT', 'UP', 'DOWN', 'BLOCK']
attacks = ['HIGH_KICK', 'LOW_KICK', 'HIGH_PUNCH', 'LOW_PUNCH']


class RandomMoveStrategy(Strategy):
    def __init__(self, player, keybd_switch, *, key_switch=None):
        super().__init__(player, keybd_switch, key_switch=key_switch)
        self._begin_time = datetime.now()
        self._working = False
        self._strat_len = 0.0

    def _random_move(self):
        move = self._key_bindings[random.choice(moves)]
        keys.press_key(move)
        time.sleep(0.05)
        keys.release_key(move)
        time.sleep(0.05)

    def _random_attack(self):
        attack = self._key_bindings[random.choice(attacks)]
        keys.press_key(attack)
        time.sleep(0.05)
        keys.release_key(attack)
        time.sleep(0.05)

    def _release(self):
        pass

    def resume(self):
        if self._working:
            return
        self._working = True
        self.loop()

    def stop(self):
        self._working = False

    def loop(self):
        while self._working:
            if self._key_switch and not self._keybd_switch.get_key_state(self._key_switch):
                self.release()
            else:
                self.do_action()
            time.sleep(0.05)

    def do_action(self):
        self._random_move()
        self._random_move()
        self._random_attack()
