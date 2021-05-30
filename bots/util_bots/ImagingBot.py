import cv2
import mss
import numpy as np
from PIL import Image as im
from win32api import GetSystemMetrics

from bots.util_bots.UtilityBot import UtilityBot
from utils import constants


class ImagingBot:
    utility_bot = UtilityBot()

    # CONVERSIONS

    @staticmethod
    def convert_nparray_to_img(nparray):
        return im.fromarray(nparray)

    @staticmethod
    def convert_nparray_array_to_img_arr(nparray_arr):
        img_arr = []
        for i in range(len(nparray_arr)):
            img_arr.append(im.fromarray(nparray_arr[i]))
        return img_arr

    @staticmethod
    def convert_img_to_nparray(img):
        return np.array(img)

    @staticmethod
    def convert_img_arr_to_nparray_arr(img_arr):
        nparray_arr = []
        for i in range(len(img_arr)):
            nparray_arr.append(np.array(img_arr[i]))
        return nparray_arr

    # SCREEN FUNCTIONS

    @staticmethod
    def get_screen_dimensions():
        return GetSystemMetrics(0), GetSystemMetrics(1)

    @staticmethod
    def get_screen_width():
        return GetSystemMetrics(0)

    @staticmethod
    def get_screen_height():
        return GetSystemMetrics(1)

    @staticmethod
    def get_screenshot():
        """
        Takes a screenshot of the target monitor configured in the constants.py file
        :return: ndarray
        """
        sct = mss.mss()
        monitor = sct.monitors[constants.TARGET_MONITOR]
        ss = sct.grab(monitor)
        return np.array(ss)

    # IMAGE MANIPULATION

    @staticmethod
    def resize_image(img, scale=0.50):
        width = int(img.shape[1] * scale)
        height = int(img.shape[0] * scale)
        dim = (width, height)
        return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    # MASKING

    @staticmethod
    def create_mask(img, lower, upper):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        res = cv2.bitwise_and(img, img, mask=mask)
        return mask, res

    @staticmethod
    def create_hsv_trackbar(window_name="Trackbars"):
        """
        Creates an HSV trackbar
        :param window_name: Name of the window. Default="Trackbars"
        :return: None
        """

        def create_trackbar_callback(x):
            pass

        cv2.namedWindow(window_name)

        cv2.createTrackbar("LH", window_name, 0, 179, create_trackbar_callback)
        cv2.createTrackbar("LS", window_name, 0, 255, create_trackbar_callback)
        cv2.createTrackbar("LV", window_name, 0, 255, create_trackbar_callback)
        cv2.createTrackbar("UH", window_name, 179, 179, create_trackbar_callback)
        cv2.createTrackbar("US", window_name, 255, 255, create_trackbar_callback)
        cv2.createTrackbar("UV", window_name, 255, 255, create_trackbar_callback)

    @staticmethod
    def get_hsv_trackbar_values(window_name="Trackbars"):
        """
        Returns the HSV values from a window containing HSV trackbars
        :param window_name: Name of the window. Default="Trackbars"
        :return: tuple. This tuple contains both the lower (index: 0), and upper (index: 1) values of a given hsv trackbar
        """
        l_h = cv2.getTrackbarPos("LH", window_name)
        l_s = cv2.getTrackbarPos("LS", window_name)
        l_v = cv2.getTrackbarPos("LV", window_name)
        u_h = cv2.getTrackbarPos("UH", window_name)
        u_s = cv2.getTrackbarPos("US", window_name)
        u_v = cv2.getTrackbarPos("UV", window_name)

        lower = np.array([l_h, l_s, l_v])
        upper = np.array([u_h, u_s, u_v])

        return lower, upper

    # DISPLAYING IMAGES

    def stack_images(self, img_arr, scale=1):
        """
        Concatenates images into a grid.
        :todo Allow different size images to be input
        :param img_arr: List of images. Can be 1 or 2 dimensional
        :param scale: scaling value
        :return: nparray
        """
        cols = len(img_arr)
        rows = len(img_arr[0])
        has_rows = isinstance(img_arr[0], list)
        if has_rows:
            for i in range(rows):
                for j in range(cols):

                    # CONVERT IMAGES TO SAME CHANNEL
                    if len(img_arr[i][j].shape) == 2:
                        img_arr[i][j] = cv2.cvtColor(img_arr[i][j], cv2.COLOR_GRAY2BGR)
                    elif img_arr[i][j].shape[2] == 4:
                        img_arr[i][j] = cv2.cvtColor(img_arr[i][j], cv2.COLOR_BGRA2BGR)

                    # SCALE IMAGE
                    img_arr[i][j] = self.resize_image(img_arr[i][j], scale / cols)
            hor = [0] * rows
            for i in range(rows):
                hor[i] = np.hstack(img_arr[i])
            ver = np.vstack(hor)
        else:
            for i in range(cols):

                # CONVERT IMAGES TO SAME CHANNEL
                if len(img_arr[i].shape) == 2:
                    img_arr[i] = cv2.cvtColor(img_arr[i], cv2.COLOR_GRAY2BGR)
                elif img_arr[i].shape[2] == 4:
                    img_arr[i] = cv2.cvtColor(img_arr[i], cv2.COLOR_BGRA2BGR)
                # SCALE IMAGE
                img_arr[i] = self.resize_image(img_arr[i], scale / cols)
            hor = np.hstack(img_arr)
            ver = hor
        return ver
