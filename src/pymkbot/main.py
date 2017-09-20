import time

from pymkbot.features.hp_feature import HPFeature
from pymkbot.features.position_feature import PositionFeature
from pymkbot.image.async_image_provider import AsyncImageProvider
from pymkbot.image.name_parser import NameParser

from pymkbot.keyboard.key_state_getter import KeyStateGetter, CAPS_LOCK, SCROLL_LOCK, KeyPressCallback
from pymkbot.strategy.lu_keng_naive_strategy import LuKengNaiveStrategy
from pymkbot.strategy.random_move_strategy import RandomMoveStrategy
from pymkbot.strategy.random_move_teacher_strategy import RandomMoveTeacherStrategy
from pymkbot.utils.async_executor import AsyncExecutor


def create_image_provider(feature_list):
    image_provider = AsyncImageProvider()
    for feature in feature_list:
        image_provider.register_consumer(feature.get_value)

if __name__ == "__main__":
    create_image_provider([PositionFeature(), HPFeature()])

    name_parser = NameParser('C:\\work\\workdir\\names')
    image_provider.register_consumer(name_parser.process_image)

    #time.sleep(5)
    strategy1 = LuKengNaiveStrategy(player=0)
    time.sleep(1)
    strategy2 = RandomMoveStrategy(player=1)
    keybd_switch = KeyStateGetter()

    keybd_shortcuts = KeyPressCallback()
    #keybd_shortcuts.add_key_callback(0x58, strat.remember)
    keybd_shortcuts.add_key_callback(0x58, strategy1.remember)
    keybd_shortcuts.add_key_callback(0x56, name_parser._calibrate)

    def run_strategy(strategy, switch=CAPS_LOCK):
        while True:
            if keybd_switch.get_key_state(switch):
                strategy.do_action()
            else:
                strategy.release()
            time.sleep(0.05)

    strategy1_executor = AsyncExecutor()
    strategy1_executor.call_soon_threadsafe(run_strategy, strategy1, SCROLL_LOCK)

    strategy2_executor = AsyncExecutor()
    strategy2_executor.call_soon_threadsafe(run_strategy, strategy2, CAPS_LOCK)

    while True:
        time.sleep(0.05)
