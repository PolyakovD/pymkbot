import numpy as np
from PIL import ImageGrab
import cv2
import time

from pymkbot.strategy import Strategy


def screen_record():
    while True:
        ps = np.array(ImageGrab.grab(bbox=(0, 30, 320, 270)))
        printscreen = cv2.resize(ps, dsize=(640, 480), interpolation=cv2.INTER_NEAREST)
        cv2.imshow('window', cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
        strat.get_action()
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


time.sleep(5)
strat =  Strategy()
screen_record()