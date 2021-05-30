import cv2 as cv
import numpy as np

from bots.util_bots.ImagingBot import ImagingBot

IMG_FILE = r'C:\Users\Amir Sharapov\Code\bots\lotro-bot-v2\testing\img.png'
img_bot = ImagingBot()

img = np.array(cv.imread(IMG_FILE))
img2 = img_bot.resize_image(img, .4)

img_arr = [img2, img]

stacked = img_bot.stack_images(img_arr, .2)
cv.imshow('hello', stacked)
cv.waitKey(0)
