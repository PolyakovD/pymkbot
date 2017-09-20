import time

import pymkbot.keyboard.directkeys as keys
from pymkbot.features.my_position_feature import MyPositionFeature
from pymkbot.image.async_image_provider import AsyncImageProvider

from pymkbot.keyboard.key_state_getter import KeyStateGetter, VK_CAPITAL, VK_SCROLL
from pymkbot.strategy.lu_keng_naive_strategy import LuKengNaiveStrategy
from pymkbot.strategy.random_move_strategy import RandomMoveStrategy
from pymkbot.utils.async_executor import AsyncExecutor

if __name__ == "__main__":

    img_provider = AsyncImageProvider()
    position_feature_provider = MyPositionFeature()
    img_provider.register_consumer(position_feature_provider.get_value)

    #time.sleep(5)
    strat = RandomMoveStrategy(keys.kbd_player1)
    time.sleep(1)
    strat2 = LuKengNaiveStrategy(keys.kbd_player2)
    #grabber.set_callback(strat.get_action)
    keybd_switch = KeyStateGetter()

    def do_strat(strategy, switch=VK_CAPITAL):
        while True:
            if keybd_switch.get_key_state(switch):
                strategy.do_action()
            time.sleep(0.05)

    strat_executor = AsyncExecutor()
    strat_executor.call_soon_threadsafe(do_strat, strat, VK_SCROLL)

    strat2_executor = AsyncExecutor()
    strat2_executor.call_soon_threadsafe(do_strat, strat2, VK_CAPITAL)

    while True:
        time.sleep(0.05)
