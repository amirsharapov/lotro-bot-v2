import time

import cv2
import numpy as np

from bots.image_processing_bot.ImageProcessingBotService import ImageProcessingBotService

imaging_bot = ImageProcessingBotService()


# imaging_bot.create_hsv_trackbar()


def find_same_image(img1, img2):
    if img1.shape[0] != img2.shape[0] or img1.shape[1] != img2.shape[1]:
        raise Exception("Images are not the same dimensions")

    masked = np.zeros_like(img1)

    for i in range(len(img1)):
        for p in range(len(img1[i])):
            if set(img1[i][p]) == set(img2[i][p]):
                masked[i][p] = (255, 255, 255)

    return masked


def main():
    while cv2.waitKey(1):

        img = imaging_bot.screenshot()

        lower, upper = imaging_bot.get_hsv_trackbar_values()

        c_mask = cv2.inRange(img, lower, upper)
        res = cv2.bitwise_and(img, img, mask=c_mask)

        c_mask = imaging_bot.resize_image(mask, .5)
        cv2.imshow('Mask', c_mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


def main2():
    print('starting')
    time.sleep(1)

    print('screenshot 1 taken')
    img = imaging_bot.screenshot()

    print('waiting')
    time.sleep(2)

    print('screenshot 2 taken')
    img2 = imaging_bot.screenshot()

    custom_mask = find_same_image(img, img2)

    return custom_mask


# main()

mask = main2()

cv2.imshow('mask', mask)
cv2.waitKey(0)
