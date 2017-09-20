from datetime import datetime
from pymkbot.strategy.strategy import Strategy
import time
import random

import pymkbot.keyboard.directkeys as keys


moves = ['LEFT', 'RIGHT', 'UP', 'DOWN', 'BLOCK']
attacks = ['HIGH_KICK', 'LOW_KICK', 'HIGH_PUNCH', 'LOW_PUNCH']


class RandomMoveTeacherStrategy(Strategy):
    def __init__(self, player, keybd_switch):
        super().__init__(player, keybd_switch)
        self._begin_time = datetime.now()
        self._strat_len = 0.0
        self._memory = []
        self._good_moves = []
        self._random_move_weight = 30
        #self._random_movement_weight = 10



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

    def _random_movement(self):
        movement = self._key_bindings[random.choice(['LEFT', 'RIGHT'])]
        self._memory.append(movement)
        keys.press_key(movement)
        time.sleep(0.25)

    def remember(self):
        moves = self._memory[-15:]
        self._good_moves.append(moves)
        print('get')
        return moves

    def add_good_moves(self, moves):
        self._good_moves.extend(moves)

    def _release(self):
        pass

    def do_action(self):
        n = random.random() * 2 * (self._random_move_weight + len(self._good_moves))
        if n > self._random_move_weight + len(self._good_moves):
            self._random_movement()
            self._random_attack()
            self._random_attack()
        elif n > self._random_move_weight:
            self._random_good_move()
        else:
            self._random_move()
            self._random_move()
            self._random_attack()
