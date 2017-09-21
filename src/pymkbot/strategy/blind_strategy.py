import datetime
import math
import pickle
import random
import time

import pymkbot.keyboard.directkeys as keys
from pymkbot.image.async_image_provider import AsyncImageProvider


def random_move():
    return random.choice(keys.moves)


def random_attack():
    return random.choice(keys.attacks)


def get_random_combination():
    return random_move(), random_move(), random_attack()


def get_random_attack_rage():
    return random_attack(), random_attack(), random_attack()


def get_random_sprint():
    return 'RUN', random.choice(['LEFT', 'RIGHT'])


def get_block():
    return 'BLOCK'


def get_down_block():
    return 'BLOCK', 'DOWN'


DUMP_SIZE = 500


class BlindStrategy:
    def __init__(self, player, keybd_switch, switch):
        self._key_bindings = keys.keyboard[player]
        self.keybd_switch = keybd_switch
        self.switch = switch

        self.player = player
        self.fighting = False
        self.working = False
        self.counter = 1
        self.log = []
        self.id = 0

    def press_moves_concurrent(self, moves, sleep_time):
        for move in moves:
            keys.press_key(self._key_bindings[move])
        time.sleep(sleep_time)
        for move in moves:
            keys.release_key(self._key_bindings[move])
        return moves, 'concurrent'

    def press_moves_sequence(self, moves, sleep_time):
        for move in moves:
            keys.press_key(self._key_bindings[move])
            time.sleep(sleep_time)
            keys.release_key(self._key_bindings[move])
        return moves, 'sequence'

    def get_players_hps(self):
        hp0, hp1 = AsyncImageProvider.get_consumer_result("hp_feature")
        return (hp0, hp1) if self.player == 0 else (hp1, hp0)

    def get_players_names(self):
        return AsyncImageProvider.get_consumer_result('name_feature')

    def get_players_dist(self):
        pos1, pos2 = AsyncImageProvider.get_consumer_result("position_feature")
        return math.fabs(pos1[0] - pos2[0])

    def combo_effectiveness(self, do_something):
        opponent_hp = self.get_players_hps()[1]
        result = do_something()
        return opponent_hp - self.get_players_hps()[1], result

    def next_combo(self, distance, my_name, vs_name):
        all_moves = [
            (get_random_sprint, True),
            (get_down_block, True),
            (get_block, True),
            (get_random_attack_rage, False),
            (get_random_combination, False)
        ]
        norm_distance = distance / 100
        weight = [norm_distance, 1, 1, math.fabs(2 - norm_distance), norm_distance]
        choice = self.weighted_choice(all_moves, weight)
        move, concurrent = choice
        if concurrent:
            return lambda x=move(), y=0.3: self.press_moves_concurrent(x, y)
        else:
            return lambda x=move(), y=0.3: self.press_moves_sequence(x, y)

    def weighted_choice(self, choices, weight):
        total = sum(weight)
        r = random.uniform(0, total)
        upto = 0
        for c, w in zip(choices, weight):
            if upto + w >= r:
                return c
            upto += w
        assert "WTF, rand doesn't work"

    def prepare(self):
        self.counter = 1
        with open('blind_bot_log.pickle', 'rb') as file:
            self.log = pickle.load(file)
        self.id = self.log[:-1]['id'] + 1

    def stop(self):
        self.fighting = False

    def resume(self):
        self.fighting = True
        if not self.working:
            self.working = True
            self.loop()

    def dump(self):
        with open('blind_bot_log.pickle', 'wb') as file:
            pickle.dump(self.log, file)

    def loop(self):
        while self.fighting:
            if not self.keybd_switch.get_key_state(self.switch):
                time.sleep(0.05)
                continue

            if self.counter % DUMP_SIZE == 0:
                self.dump()

            distance = self.get_players_dist()
            my_name, vs_name = self.get_players_names()
            my_hp, vs_hp = self.get_players_hps()

            next_combo = self.next_combo(distance, my_name, vs_name)
            now = datetime.datetime.now()

            hp, combo = self.combo_effectiveness(next_combo)
            self.log.append({
                'diff_hp': hp,
                'combo': combo,
                'my_name': my_name,
                'vs_name': vs_name,
                'distance': distance,
                'my_hp': my_hp,
                'vs_hp': vs_hp,
                'timestamp': now,
                'id': self.id
            })
            self.id += 1
        self.working = True
        self.dump()
