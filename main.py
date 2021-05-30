from time import time

import cv2
import cv2 as cv
import numpy

from bots.util_bots.ImagingBot import ImagingBot

bot = ImagingBot()


def capture_screen_object_recognition():
    loop_time = time();

    bot.create_canny_trackbar()
    # bot.create_hsv_trackbar()

    blank = bot.get_blank_image(1080, 1920)
    # blank = bot.get_blank_image()

    while True:

        thresh_1, thresh_2 = bot.get_canny_trackbar_values()
        # lower, upper = bot.get_hsv_trackbar_values()

        img = bot.get_screenshot()
        img_contour = img.copy()
        img_blurred = cv.GaussianBlur(img, (7, 7), 2)
        # _, img_res = bot.get_mask(img, lower, upper)
        img_grayed = cv.cvtColor(img_blurred, cv.COLOR_BGR2GRAY)
        img_canny = cv.Canny(img_grayed, thresh_1, thresh_2, )
        img_dil = cv2.dilate(img_canny, numpy.ones((5,5)), iterations=1)

        bot.get_contours(img_dil, img_contour)

        img_array = [[img, img_blurred, img_grayed],
                     [img_canny, img_dil, img_contour]]

        img_stack = bot.stack_images(img_array, .8)

        cv.imshow(" ", img_stack)

        print(f"FPS: {1 / (time() - loop_time)}")
        loop_time = time()

        # SET BREAK
        if cv.waitKey(1) & 0xFF == ord('q'):
            cv.destroyAllWindows()
            break


def capture_screen_with_mask():
    loop_time = time()
    bot.create_hsv_trackbar()
    while True:

        # GET IMAGE
        img = bot.get_screenshot()
        img = bot.resize_image(img, 0.6)

        # CREATE MASK USING TRACKBAR (TEMP FOR TESTING)
        lower, upper = bot.get_hsv_trackbar_values()
        mask, res = bot.get_mask(img, lower, upper)

        # SHOW EACH IMAGE
        cv.imshow("Image", img)
        cv.imshow("Mask", mask)
        cv.imshow("Result", res)

        print(f"FPS: {1 / (time() - loop_time)}")
        loop_time = time()

        # SET BREAK
        if cv.waitKey(1) & 0xFF == ord('q'):
            cv.destroyAllWindows()
            break


capture_screen_object_recognition()