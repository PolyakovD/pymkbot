import pickle
import time

from pymkbot.features.my_position_feature import MyPositionFeature
from pymkbot.image.async_image_provider import AsyncImageProvider

from pymkbot.keyboard.key_state_getter import KeyStateGetter, CAPS_LOCK, SCROLL_LOCK, KeyPressCallback
from pymkbot.strategy.random_move_strategy import RandomMoveStrategy
from pymkbot.strategy.random_move_teacher_strategy import RandomMoveTeacherStrategy
from pymkbot.utils.async_executor import AsyncExecutor

SPACE = 0x20
ENTER = 0x0D


if __name__ == "__main__":
    image_provider = AsyncImageProvider()
    position_feature_provider = MyPositionFeature()
    image_provider.register_consumer(position_feature_provider.get_value)

    data = {}

    def run_data_collection():
        centers = position_feature_provider.centers
        print('first histogram center coordinates x={}, y={}'.format(centers[0, 1], centers[0, 0]))
        print('second histogram center coordinates x={}, y={}'.format(centers[1, 1], centers[1, 0]))
        name0 = input("Enter first hero name: ")
        name1 = input("Enter second hero name: ")
        data[name0] = position_feature_provider.histogram0
        data[name1] = position_feature_provider.histogram0

    def pickle_data():
        with open('data.pickle', 'wb') as file:
            pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)


    with open('data.pickle', 'rb') as file:
        data = pickle.load(file)
    print(data.keys())

    keybd_shortcuts1 = KeyPressCallback()
    keybd_shortcuts1.add_key_callback(SPACE, run_data_collection)
    keybd_shortcuts2 = KeyPressCallback()
    keybd_shortcuts2.add_key_callback(ENTER, pickle_data)

    while True:
        time.sleep(0.05)
