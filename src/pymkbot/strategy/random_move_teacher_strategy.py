from datetime import datetime
from pymkbot.strategy.strategy import Strategy
import time
import random

import pymkbot.keyboard.directkeys as keys


moves = ['LEFT', 'RIGHT', 'UP', 'DOWN', 'BLOCK']
attacks = ['HIGH_KICK', 'LOW_KICK', 'HIGH_PUNCH', 'LOW_PUNCH']


class RandomMoveTeacherStrategy(Strategy):
    def __init__(self, key_bindings):
        super().__init__(key_bindings)
        self._begin_time = datetime.now()
        self._strat_len = 0.0
        self._memory = []
        self._good_moves = []

    def _random_move(self):
        move = self._key_bindings[random.choice(moves)]
        self._memory.append(move)
        keys.press_key(move)
        time.sleep(0.05)
        keys.release_key(move)
        time.sleep(0.05)

    def _random_attack(self):
        attack = self._key_bindings[random.choice(attacks)]
        self._memory.append(attack)
        keys.press_key(attack)
        time.sleep(0.05)
        keys.release_key(attack)
        time.sleep(0.05)

    def _random_good_move(self):
        if not self._good_moves:
            return
        seq = random.choice(self._good_moves)
        for action in seq:
            self._memory.append(action)
            keys.press_key(action)
            time.sleep(0.05)
            keys.release_key(action)
            time.sleep(0.05)

    def remember(self):
        self._good_moves.append(self._memory[-20:])
        print('get')

    def _release(self):
        pass

    def do_action(self):
        if random.random() * (10 + len(self._good_moves)) > 10:
            self._random_good_move()
        else:
            self._random_move()
            self._random_move()
            self._random_attack()



