import time

from pymkbot.image.async_image_grab import AsyncImageGrabber
from pymkbot.strategy.empty_strategy import EmptyStrategy
import pymkbot.keyboard.directkeys as keys

from pymkbot.keyboard.key_state_getter import KeyStateGetter, VK_CAPITAL
from pymkbot.strategy.lu_keng_naive_strategy import LuKengNaiveStrategy
from pymkbot.strategy.naive_strategy import NaiveStrategy
from pymkbot.strategy.random_move_strategy import RandomMoveStrategy
from pymkbot.utils.async_executor import AsyncExecutor

if __name__ == "__main__":

    grabber = AsyncImageGrabber()
    grabber.begin_recording()

    #time.sleep(5)
    strat = RandomMoveStrategy(keys.kbd_player1)
    time.sleep(1)
    strat2 = RandomMoveStrategy(keys.kbd_player2)
    #grabber.set_callback(strat.get_action)
    keybd_switch = KeyStateGetter()

    def do_strat(strategy):
        while True:
            if keybd_switch.get_key_state(VK_CAPITAL):
                strategy.do_action()
            time.sleep(0.05)

    strat_executor = AsyncExecutor()
    strat_executor.call_soon_threadsafe(do_strat, strat)

    strat2_executor = AsyncExecutor()
    strat2_executor.call_soon_threadsafe(do_strat, strat2)

    while True:
        time.sleep(0.05)
