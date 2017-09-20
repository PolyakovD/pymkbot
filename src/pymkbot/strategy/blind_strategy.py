import random

import time

from pymkbot.image.async_image_provider import AsyncImageProvider
from pymkbot.strategy.strategy import Strategy
import pymkbot.keyboard.directkeys as keys


def random_move():
    return random.choice(keys.moves)


def random_attack():
    return random.choice(keys.attacks)


def get_random_combination():
    return random_move(), random_move(), random_attack()


def get_random_sprint():
    return 'RUN', random.choice(['LEFT', 'RIGHT'])


def get_random_attack_rage():
    return random_attack(), random_attack(), random_attack()


def get_block():
    return 'BLOCK'


def get_down_block():
    return 'BLOCK', 'DOWN'


class BlindStrategy(Strategy):
    def __init__(self, player, keybd_switch):
        super().__init__(player, keybd_switch)

    def _release(self):
        pass

    def press_moves_concurrent(self, moves, sleep_time):
        for move in moves:
            keys.press_key(self._key_bindings[move])
        time.sleep(sleep_time)
        for move in moves:
            keys.release_key(self._key_bindings[move])

    def press_moves_sequence(self, moves, sleep_time):
        for move in moves:
            keys.press_key(self._key_bindings[move])
            time.sleep(sleep_time)
            keys.release_key(self._key_bindings[move])

    def get_opponent_hp(self):
        hp0, hp1 = AsyncImageProvider.get_consumer_result("hp_feature")
        return hp1 if self._player == 0 else hp0

    def combo_effectiveness(self, do_something):
        opponent_hp = self.get_opponent_hp()
        do_something()
        return opponent_hp - self.get_opponent_hp()

    def run_strategy(self, switch):
        counter = 1
        while True:
            if counter % 500 == 0:
                self.dump_data()




            counter += 1




