import pickle
import time

from pymkbot.features.position_feature import PositionFeature
from pymkbot.image.async_image_provider import AsyncImageProvider
from pymkbot.keyboard.key_state_getter import KeyPressCallback

SPACE = 0x20
ENTER = 0x0D


if __name__ == "__main__":
    image_provider = AsyncImageProvider()
    position_feature_provider = PositionFeature()
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
        with open('character_histogram.pickle', 'wb') as file:
            pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)


    with open('character_histogram.pickle', 'rb') as file:
        data = pickle.load(file)
    print(data.keys())
    # print(data["scorpion"].shape)

    keybd_shortcuts = KeyPressCallback()
    keybd_shortcuts.add_key_callback(SPACE, run_data_collection)
    keybd_shortcuts.add_key_callback(ENTER, pickle_data)

    while True:
        time.sleep(0.05)
