from time import time

import cv2 as cv

from bots.util_bots.ImagingBot import ImagingBot

bot = ImagingBot()


def capture_screen_object_recognition():
    loop_time = time();

    while True:
        img = bot.get_screenshot()
        img_scaled = bot.resize_image(img)
        img_blurred = cv.GaussianBlur(img_scaled, (7, 7), 1)
        img_grayed = cv.cvtColor(img_blurred, cv.COLOR_BGR2GRAY)

        cv.imshow(" ", img_grayed)

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
        mask, res = bot.create_mask(img, lower, upper)

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
