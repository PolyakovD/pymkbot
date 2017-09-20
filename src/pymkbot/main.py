import time

from pymkbot.features.hp_feature import HPFeature
from pymkbot.features.name_feature import NameFeature
from pymkbot.features.position_feature import PositionFeature
from pymkbot.image.async_image_provider import AsyncImageProvider
from pymkbot.keyboard.key_state_getter import KeyStateGetter, CAPS_LOCK, SCROLL_LOCK, KeyPressCallback
from pymkbot.strategy.random_move_strategy import RandomMoveStrategy
from pymkbot.strategy.random_move_teacher_strategy import RandomMoveTeacherStrategy
from pymkbot.utils.good_moves_serializer import GoodMovesSerializer
from pymkbot.utils.params_config import read_config
from pymkbot.utils.async_executor import AsyncExecutor


def create_image_provider(feature_list, debug_image_size):
    AsyncImageProvider.launch(debug_image_size=debug_image_size)
    for feature in feature_list:
        AsyncImageProvider.register_consumer(feature.get_name(), feature.get_value)


if __name__ == "__main__":
    params_config = read_config('config.yml')

    name_feature = NameFeature(params_config.nameplates_path)
    image_provider = create_image_provider([PositionFeature(), HPFeature(), name_feature], params_config.debug_image_size)

    #image_provider.register_consumer(name_parser.process_image)


    strategy1 = RandomMoveTeacherStrategy(player=0)
    time.sleep(1)
    strategy2 = RandomMoveStrategy(player=1)
    keybd_switch = KeyStateGetter()

    #moves_serializer = GoodMovesSerializer(strategy1, image_provider, params_config.moves_lib_path)
    #moves_serializer.load()

    keybd_shortcuts = KeyPressCallback()
    #keybd_shortcuts.add_key_callback(0x58, moves_serializer.on_save_coomand)
    # keybd_shortcuts.add_key_callback(0x5A, name_feature._calibrate)

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
