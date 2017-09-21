import random
import time

import asyncio

from pymkbot.image.async_image_provider import AsyncImageProvider
from pymkbot.keyboard.key_state_getter import KeyStateGetter, CAPS_LOCK, SCROLL_LOCK
from pymkbot.utils.async_executor import AsyncExecutor
from pymkbot.utils.menu_control import MenuControl


class Metastrategy:
    def __init__(self):
        self._executor = AsyncExecutor()
        self._menucontrol = MenuControl()
        self._key_state_getter = KeyStateGetter()
        self._strategies = {}
        self._is_halt = True
        self._is_running = False
        self._idx = 0

    def _run_strategy(self, strategy):
        strategy.prepare()
        strategy.stop()
        if not self._is_halt:
            strategy.resume()

    def add_strategy(self, strategy):
        executor = AsyncExecutor()
        executor.call_soon_threadsafe(self._run_strategy, strategy)
        self._strategies[self._idx] = executor, strategy
        self._idx += 1

    def _halt(self):
        if self._is_halt:
            return
        self._is_halt = True
        for _, strategy in self._strategies.values():
            strategy.stop()

    def _unhalt(self):
        if not self._is_halt:
            return
        self._is_halt = False
        for executor, strategy in self._strategies.values():
            executor.call_soon_threadsafe(strategy.resume)

    def _check_menu(self):
        current_menu_state = AsyncImageProvider.get_consumer_result('menu_feature')
        if current_menu_state == 'not_menu':
            return False
        self._halt()
        if current_menu_state == 'menu_fail':
            self._menucontrol.start()
        if current_menu_state == 'menu_char':
            self._menucontrol.move('UP')
            self._menucontrol.select()
        if current_menu_state == 'menu_main':
            self._menucontrol.select()
        if current_menu_state == 'menu_mode':
            self._menucontrol.select()
        if current_menu_state == 'menu_towers':
            for i in range(0, int(random.random() * 6)):
                self._menucontrol.move('RIGHT')
            self._menucontrol.select()
        return True

    def _check_battle(self):
        name0, name1 = AsyncImageProvider.get_consumer_result('name_feature')
        if name0 is None and name1 is None:
            return
        self._unhalt()

    def _run(self):
        self._is_running = True
        while True:
            time.sleep(0.05)
            both_off = not (self._key_state_getter.get_key_state(CAPS_LOCK) or self._key_state_getter.get_key_state(SCROLL_LOCK))
            if both_off:
                continue
            if self._check_menu():
                continue
            self._check_battle()

    def run(self):
        self._executor.call_soon_threadsafe(self._run)