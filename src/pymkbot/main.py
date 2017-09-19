import time

from pymkbot.image.async_image_grab import AsyncImageGrabber
from pymkbot.strategy.empty_strategy import EmptyStrategy

from pymkbot.keyboard.key_state_getter import KeyStateGetter, VK_CAPITAL

if __name__ == "__main__":

    grabber = AsyncImageGrabber()
    grabber.begin_recording()

    time.sleep(5)
    strat = EmptyStrategy()
    #grabber.set_callback(strat.get_action)
    keybd_switch = KeyStateGetter()
    while True:
        #if keybd_switch.get_key_state(VK_CAPITAL):
        #    strat.get_action()
        time.sleep(0.05)
