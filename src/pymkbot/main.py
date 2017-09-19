import time
import msvcrt

from pymkbot.image.async_image_grab import AsyncImageGrabber
from pymkbot.stategy.empty_strategy import EmptyStrategy


if __name__ == "__main__":

grabber = AsyncImageGrabber()
grabber.begin_recording()

time.sleep(5)
strat = EmptyStrategy()
#grabber.set_callback(strat.get_action)



while True:
    x = get_capslock_state()
    if x % 2:
        strat.get_action()
    time.sleep(0.05)
