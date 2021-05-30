import time

import cv2
import numpy as np

from bots.util_bots.ImagingBot import ImagingBot

bot = ImagingBot()

while True:
    img = bot.get_screenshot()
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blank = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

    img_arr = [[img, img2], [img, blank]]
    stacked = bot.stack_images(img_arr, .5)

    cv2.imshow('stacked', stacked)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()