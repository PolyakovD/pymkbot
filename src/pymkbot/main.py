import numpy as np
from PIL import ImageGrab
import cv2


def screen_record():
    #last_time = time.time()
    while(True):
        # 800x600 windowed mode for GTA 5, at the top left position of your main screen.
        # 40 px accounts for title bar.
        ps = np.array(ImageGrab.grab(bbox=(0,30,320,270)))
        printscreen = cv2.resize(ps, dsize=(640, 480), interpolation=cv2.INTER_NEAREST)
        #print('loop took {} seconds'.format(time.time()-last_time))
        #last_time = time.time()
        cv2.imshow('window',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

screen_record()
