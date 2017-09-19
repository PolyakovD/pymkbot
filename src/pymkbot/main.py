import numpy as np
from PIL import ImageGrab
import cv2

from pymkbot.keyboard.directkeys import W, A, S, D, press_key, release_key


def screen_record():
    while True:
        ps = np.array(ImageGrab.grab(bbox=(0, 30, 320, 270)))
        printscreen = cv2.resize(ps, dsize=(640, 480), interpolation=cv2.INTER_NEAREST)
        cv2.imshow('window', cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

            
def do_some_moves():
    while (True):
        time.sleep(1)
        release_key(0x11)

        
screen_record()
