from ctypes import windll

import cv2
import mss
import numpy as np
import win32gui
import win32ui
from PIL import Image
from win32api import GetSystemMetrics

from utils import constants


class ImageProcessingBotService:
    def __init__(self):
        """
        Runs on class initialization
        """
        self.target_monitor_width = self.get_screen_width()
        self.target_monitor_height = self.get_screen_height()

    # CONVERSIONS

    @staticmethod
    def convert_to_bgr(img):
        """
        Converts an image to BGR from BGRA or Grayscale
        :param img: Image to convert
        :return: nparray
        """
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

    # SCREEN FUNCTIONS

    @staticmethod
    def get_screen_dimensions():
        """
        Gets the height and width of the screen
        :return: tuple
        """
        return GetSystemMetrics(0), GetSystemMetrics(1)

    @staticmethod
    def get_screen_width():
        """
        Get the wdith of the screen
        :return: integer
        """
        return GetSystemMetrics(0)

    @staticmethod
    def get_screen_height():
        """
        Get the height of the screen
        :return: integer
        """
        return GetSystemMetrics(1)

    # noinspection PyTypeChecker
    def screenshot(self):
        """
        Takes a screenshot of the monitor defined in the constants file
        :return: ndarray
        """
        sct = mss.mss()
        monitor = sct.monitors[constants.TARGET_MONITOR]
        return self.convert_to_bgr(
            np.array(
                sct.grab(monitor)
            )
        )

    @staticmethod
    def screenshot_window(window_name=constants.LOTRO_WINDOW):
        """
        Takes a screenshot of a window (Default=Lotro Window)
        :param window_name: Name of the window to take screenshot of
        :return: npArray
        :TODO -> Understand and comment the code
        """
        # SOURCE CODE:
        # https://stackoverflow.com/questions/19695214/python-screenshot-of-inactive-window-printwindow-win32gui/24352388#24352388

        hwnd = win32gui.FindWindow(None, window_name)

        # GET DIMENSIONS
        x, y, right, bottom = win32gui.GetWindowRect(hwnd)
        w = right - x
        h = bottom - y

        # WINDOW CONTEXT
        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        # BITMAP
        bit_map = win32ui.CreateBitmap()
        bit_map.CreateCompatibleBitmap(mfc_dc, w, h)

        save_dc.SelectObject(bit_map)
        result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 0)
        bmp_info = bit_map.GetInfo()
        bmp_str = bit_map.GetBitmapBits(True)

        img = Image.frombuffer(
            'RGB',
            (bmp_info['bmWidth'], bmp_info['bmHeight']),
            bmp_str, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(bit_map.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)

        # IF SUCCESS
        if result == 1:
            return cv2.cvtColor(
                np.array(img),
                cv2.COLOR_RGB2BGR
            )

    def get_img_segment(self, img, rect=(0, 0, 0, 0)):
        """
        (npArray) -> (npArray)
        Get a segment of an image
        :param img: Source of the image as type: np
        :param rect: x, y, h, w coordinates of the segement
        :return: nparray
        """
        x, y, w, h = rect
        img = self.convert_to_bgr(img)
        if w == 0:
            w = self.target_monitor_width
        if w == 0:
            h = self.target_monitor_height

        return img[y:y + h, x:x + w]

    # IMAGE MANIPULATION

    @staticmethod
    def resize_image(img, scale=0.5):
        """
        Resizes the image
        :param img: Image to resize
        :param scale: Multiplier of the resize
        :return: npArray
        """
        width = int(img.shape[1] * scale)
        height = int(img.shape[0] * scale)
        dim = (width, height)
        return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    # WINDOWS

    def create_window(self, window_name):
        """
        Creates a window if a window of the same name is not open
        :param window_name: Name of the window
        :return: None
        """
        if not self.is_window_open(window_name):
            cv2.namedWindow(window_name)

    @staticmethod
    def is_window_open(window_name):
        """
        Checks if a window is open
        :param window_name: Name of the window to check
        :return: boolean
        """
        if cv2.getWindowImageRect(window_name) == (-1, -1, -1, -1):
            return False
        return True

    # TRACKBARS - CREATE

    @staticmethod
    def do_nothing(x=None):
        """
        Does nothing
        :param x: Param (Default=None)
        :return: None
        """
        pass

    def create_canny_trackbar(self, default_th1=0, default_th2=0, window_name="Canny"):
        """
        Creates a trackbar for manipulating the Canny effect on an image
        :param default_th1: Default threshold for threshold 1 (Default=0)
        :param default_th2: Default threshold for threshold 2 (Default=0)
        :param window_name: Name of the window (Default="Canny")
        :return: None
        """
        self.create_window(window_name)
        cv2.createTrackbar("TH1", window_name, default_th1, 255, self.do_nothing)
        cv2.createTrackbar("TH2", window_name, default_th2, 255, self.do_nothing)

    def create_contour_trackbar(self, default_min_area=1000, default_max_area=0, window_name="Contour"):
        """
        Creates trackbars to manipulate the contour of an image
        :param default_min_area: Default minimum area
        :param default_max_area: Default maximum area
        :param window_name: Name of the window to set the trackbars
        :return: None
        """
        if default_max_area == 0:
            default_max_area = int(self.get_screen_width() * self.get_screen_height() / 10)
        self.create_window(window_name)
        cv2.createTrackbar("Min Area", window_name, default_min_area, default_max_area, self.do_nothing)
        cv2.createTrackbar("Max Area", window_name, default_max_area, default_max_area, self.do_nothing)

    def create_dilation_trackbar(self, default_kernel=5, default_iterations=1, window_name="Dilate"):
        """
        Creates trackbars to manipulate dilation values
        :param default_kernel: Kernal
        :param default_iterations: Iterations
        :param window_name: Name of the window to set the trackbars
        :return: None
        """
        self.create_window(window_name)
        cv2.createTrackbar("D - KERN", window_name, default_kernel, 25, self.do_nothing)
        cv2.createTrackbar("D - ITER", window_name, default_iterations, 25, self.do_nothing)

    def create_erosion_trackbar(self, default_kernel=5, default_iterations=1, window_name="Erode"):
        """
        Creates trackbars to manipulate erosion values
        :param default_kernel: Kernel
        :param default_iterations: Iterations
        :param window_name: Name of the window to set the trackbars
        :return: None
        """
        self.create_window(window_name)
        cv2.createTrackbar("E - KERN", window_name, default_kernel, 25, self.do_nothing)
        cv2.createTrackbar("E - ITER", window_name, default_iterations, 25, self.do_nothing)

    def create_gaussian_blur_trackbar(self, default_kernel=7, default_sigma_x=3, window_name="Gaussian Blur"):
        """
        Creates trackbars to manipulate gaussian blur values
        :param default_kernel: Default value for the kernel trackbar
        :param default_sigma_x: Default value for the sigma_x trackbar
        :param window_name: Name of the window to set the trackbars
        :return: None
        """
        self.create_window(window_name)
        cv2.createTrackbar("GB - Kernel", window_name, default_kernel, 25, self.do_nothing)
        cv2.createTrackbar("GB - Sigma X", window_name, default_sigma_x, 100, self.do_nothing)

    def create_hsv_trackbar(self, default_lh=0, default_ls=0, default_lv=0, default_uh=179, default_us=255,
                            default_uv=255, window_name="HSV"):
        """
        Creates trackbars to manipulate hsv lower and upper values
        :param default_lh: The default lower hue value (Default=0)
        :param default_ls: The default lower saturation value (Default=0)
        :param default_lv: The default lower value (Default=0)
        :param default_uh: The default upper hue value (Default 179)
        :param default_us: The default upper saturation value (Default 255)
        :param default_uv: The default upper value (Default 255)
        :param window_name: The name of the window
        :return: None
        """

        self.create_window(window_name)

        cv2.createTrackbar("LH", window_name, default_lh, 179, self.do_nothing)
        cv2.createTrackbar("LS", window_name, default_ls, 255, self.do_nothing)
        cv2.createTrackbar("LV", window_name, default_lv, 255, self.do_nothing)
        cv2.createTrackbar("UH", window_name, default_uh, 179, self.do_nothing)
        cv2.createTrackbar("US", window_name, default_us, 255, self.do_nothing)
        cv2.createTrackbar("UV", window_name, default_uv, 255, self.do_nothing)

    def create_rectangle_trackbar(self, default_x=0, default_y=1, default_width=100, default_height=100,
                                  window_name="Rectangle"):
        """
        Creates trackbars to alter a rectangle
        :param default_x: Top value of rectangle
        :param default_y: Left value of rectangle
        :param default_width: Width value of rectangle
        :param default_height: Height value of rectangle
        :param window_name: Name of window trackbars should be located
        :return: None
        """
        cv2.createTrackbar("X", window_name, default_x, 1920, self.do_nothing)
        cv2.createTrackbar("Y", window_name, default_y, 1080, self.do_nothing)
        cv2.createTrackbar("W", window_name, default_width, 1920, self.do_nothing)
        cv2.createTrackbar("H", window_name, default_height, 1080, self.do_nothing)

    def create_segmentation_trackbar(self, default_x=0, default_y=0, default_size=5, window_name="Segmentation"):
        """
        Creates trackbars to manipulate a segmented image size and position values
        :param default_x: The default value for the X trackbar value (Default=0)
        :param default_y: The default value for the Y trackbar value (Default=0)
        :param default_size: Default percentage
        :param window_name: The name of the window (Default="Segmentation"
        :return: None
        """

        self.create_window(window_name)

        cv2.createTrackbar("X", window_name, default_x, self.target_monitor_width, self.do_nothing)
        cv2.createTrackbar("Y", window_name, default_y, self.target_monitor_height, self.do_nothing)
        cv2.createTrackbar("Size", window_name, default_size, 100, self.do_nothing)

    def create_brightness_trackbar(self, default_brightness=0, window_name="Brightness"):
        """
        Creates trackbars to manipulate brightness value
        :param default_brightness: Default brightness to set the trackbar
        :param window_name: Name of the window
        :return: None
        """
        self.create_window(window_name)
        cv2.createTrackbar('Brightness L', window_name, default_brightness, 255, self.do_nothing)

    def create_contrast_trackbar(self, default_contrast=0, window_name="Contrast"):
        """
        Create trackbar to manipulate contrast value
        :param default_contrast: Default contrast to set the tracker
        :param window_name: Name of the window
        :return:
        """
        self.create_window(window_name)
        cv2.createTrackbar("Contrast L", window_name, default_contrast, 130, self.do_nothing)

    # TRACKBARS - GET VALUES

    @staticmethod
    def get_canny_trackbar_values(window_name="Canny"):
        """
        Method to get the canny values
        :param window_name: Name of the window trackbars are lcoated
        :return: integer, integer
        """
        threshold_1 = cv2.getTrackbarPos("TH1", window_name)
        threshold_2 = cv2.getTrackbarPos("TH2", window_name)

        return threshold_1, threshold_2

    @staticmethod
    def get_contour_trackbar_values(window_name="Contour"):
        """
        Method to get the contour values
        :param window_name: Name of the window trackbars are located
        :return: integer, integer
        """
        min_area = cv2.getTrackbarPos("Min Area", window_name)
        max_area = cv2.getTrackbarPos("Max Area", window_name)

        return min_area, max_area

    @staticmethod
    def get_dilation_trackbar_values(window_name="Dilate"):
        """
        Method to get the dilation values
        :param window_name: Name of the window trackbars are located
        :return: Tuple, integer
        """
        kernel_value = cv2.getTrackbarPos("D - KERN", window_name)
        if kernel_value % 2 != 1:
            kernel_value += 1

        kernel = np.ones((kernel_value, kernel_value), np.uint8)
        iterations = cv2.getTrackbarPos("D - ITER", window_name)

        return kernel, iterations

    @staticmethod
    def get_erosion_trackbar_values(window_name="Erode"):
        """
        Method to get the erosion values
        :param window_name: Name of the window trackbars are located
        :return: Tuple, integer
        """
        kernel_value = cv2.getTrackbarPos("E - KERN", window_name)
        if kernel_value % 2 != 1:
            kernel_value += 1

        kernel = np.ones((kernel_value, kernel_value), np.uint8)
        iterations = cv2.getTrackbarPos("E - ITER", window_name)

        return kernel, iterations

    @staticmethod
    def get_gaussian_blur_trackbar_values(window_name="Gaussian Blur"):
        """
        Method to get the gaussian blur values
        :param window_name: Name of the window trackbars are located
        :return: Tuple, integer
        """
        kernel_value = cv2.getTrackbarPos("GB - Kernel", window_name)
        if kernel_value % 2 != 1:
            kernel_value += 1

        kernel = (kernel_value, kernel_value)
        sigma_x = cv2.getTrackbarPos("GB - Sigma X", window_name)

        return kernel, sigma_x

    @staticmethod
    def get_hsv_trackbar_values(window_name="HSV"):
        """
        Method to get the HSV values from a window containing HSV trackbars
        :param window_name: Name of the window. Default="HSV"
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

    @staticmethod
    def get_rectangle_trackbar_values(window_name="Rectangle"):
        """
        Method to get the size and position values of a rectangle
        :param window_name: Name of the window
        :return: None
        """
        x = cv2.getTrackbarPos("X", window_name)
        y = cv2.getTrackbarPos("Y", window_name)
        width = cv2.getTrackbarPos("W", window_name)
        height = cv2.getTrackbarPos("H", window_name)

        return x, y, width, height

    @staticmethod
    def get_segmentation_trackbar_values(window_name="Segmentation"):
        """
        Method to get the value of the segmented section of the image
        :param window_name: Name of the window the trackbar is located
        :return: integer, integer, integer
        """
        x = cv2.getTrackbarPos("X", window_name)
        y = cv2.getTrackbarPos("Y", window_name)
        size = cv2.getTrackbarPos("Size", window_name)

        return x, y, size

    @staticmethod
    def get_brightness_trackbar_value(window_name="Brightness"):
        """
        Method to get the value of the brightness trackbar
        :param window_name: Name of the window the trackbar is located
        :return: integer
        """
        return cv2.getTrackbarPos('Brightness L', window_name)

    @staticmethod
    def get_contrast_trackbar_value(window_name="Contrast"):
        """
        Method to get the value of the contrast trackbar
        :param window_name: Name of the window the trackbar is located
        :return: integer
        """
        return cv2.getTrackbarPos("Contrast L", window_name)

    # PROCESSING

    @staticmethod
    def gaussian_blur(img, kernel=(7, 7), sigma_x=2):
        """
        Blurs an image using Gaussian blur
        :param img: Image to blur
        :param kernel: Size of the kernel
        :param sigma_x: Gaussian kernel standard deviation in the x direction
        :return: npArray
        """
        return cv2.GaussianBlur(img, kernel, sigma_x)

    @staticmethod
    def mask(img, lower, upper):
        """
        Method to handle masking an image
        :param img: Image to mask
        :param lower: Lower HSV value threshold to define mask
        :param upper: Upper HSV value threshold to define mask
        :return: npArray (of the image AFTER masking)
        """
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        res = cv2.bitwise_and(img, img, mask=mask)
        return res

    def gray(self, img):
        """
        Method to handle grayscaling an image
        :param img: Image to process
        :return: npArray
        """
        return self.convert_to_bgr(
            cv2.cvtColor(
                self.convert_to_bgr(img),
                cv2.COLOR_BGR2GRAY
            )
        )

    @staticmethod
    def canny(img, threshold_1, threshold_2):
        """
        Method to handle cannying the image
        :param img: Image to process
        :param threshold_1: Threshold 1
        :param threshold_2: Threshold 2
        :return: npArray
        """
        return cv2.Canny(img, threshold_1, threshold_2)

    @staticmethod
    def dilate(img, kernel=np.ones((5, 5)), iterations=1):
        """
        Method to handle dilating the image after canny
        :param img: Image to process
        :param kernel: Kernel
        :param iterations: Iterations
        :return: npArray
        """
        return cv2.dilate(img, kernel, iterations=iterations)

    @staticmethod
    def erode(img, kernel=np.ones((5, 5)), iterations=1):
        """
        Method to handle eroding the image after canny
        :param img: Image to process
        :param kernel: Kernel
        :param iterations: Iterations
        :return: npArray
        """
        return cv2.erode(img, kernel, iterations=iterations)

    @staticmethod
    def adjust_brightness(img, brightness=0):
        """
        Method to handle processing the brightness of an image
        :param img: Image to process
        :param brightness: Level of contrast
        :return: npArray
        """
        if brightness != 0:
            if brightness > 0:
                shadow = brightness
                highlight = 255
            else:
                shadow = 0
                highlight = 255 + brightness
            alpha_b = (highlight - shadow) / 255
            gamma_b = shadow

            return cv2.addWeighted(img, alpha_b, img, 0, gamma_b)
        else:
            return img.copy()

    @staticmethod
    def adjust_contrast(img, contrast=0):
        """
        Method to handle processing the contrast of an image
        :param img: Image to process
        :param contrast: Level of contrast
        :return: npArray
        """
        if contrast != 0:
            f = 131 * (contrast + 127) / (127 * (131 - contrast))
            alpha_c = f
            gamma_c = 127 * (1 - f)

            return cv2.addWeighted(img, alpha_c, img, 0, gamma_c)

        return img.copy()

    # CONTOURS

    @staticmethod
    def draw_rectangle(img, rect, color=(0, 255, 0), thickness=3):
        """
        Draws a rectangle on an image
        :param img: The image to draw the rectangle on
        :param rect: Tuple of top, left, right, bottom positions
        :param color: Color of rectangle
        :param thickness: Thickness of the rectangle. -1 will fill
        :return: None
        """
        x, y, width, height = rect
        cv2.rectangle(img, (x, y), (x + width, y + height), color, thickness=thickness)

    def draw_contours(self, img, img_contour, min_area=1000, max_area=None):
        """
        Draws contours on an image
        :param img: Image to detect contours
        :param img_contour: Image to draw contours on
        :param min_area: Minimum area to detect contour
        :param max_area: Maximum area to detect contour
        :return: Tuples (x, y, w, h)
        """
        if max_area is None:
            max_area = int(self.get_screen_width() * self.get_screen_height() / 10)
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        rects = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if min_area < area < max_area:
                cv2.drawContours(img_contour, cnt, -1, (255, 0, 255), 2)
                perimeter = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
                x, y, w, h = cv2.boundingRect(approx)
                rects.append((x, y, w, h))

                self.draw_rectangle(img_contour, (x, y, w, h))

                self.write_text(img_contour, f'Points: {len(approx)}', (x + w + 10, y + 20))
                self.write_text(img_contour, f'Area: {int(area)}', (x + w + 10, y + 35))
        return rects

    # DISPLAYING IMAGES

    def get_blank_image(self, height=None, width=None, channels=3):
        """
        Creates a blank image as a placeholder
        :param height: Height of the blank image
        :param width: Width of the blank image
        :param channels: Count of channels of the blank image
        :return: None
        """
        if height is None:
            height = self.get_screen_height()
        if width is None:
            width = self.get_screen_width()
        return np.zeros((height, width, channels), np.uint8)

    def stack_images(self, img_arr, scale=1):
        """
        Concatenates images into a grid.
        :param img_arr: List of images. Can be 1 or 2 dimensional
        :param scale: scaling value
        :return: nparray
        """
        x = len(img_arr)
        y = len(img_arr[0])
        z = max(x, y)
        is_2d = isinstance(img_arr[0], list)
        if is_2d:

            resize_width = int(img_arr[0][0].shape[1] * scale / z)
            resize_height = int(img_arr[0][0].shape[0] * scale / z)

            for i in range(0, x):
                for j in range(0, y):
                    # CONVERT IMAGES TO SAME SIZE - IF ALREADY SAME SIZE, NOTHING CHANGES
                    img_arr[i][j] = cv2.resize(img_arr[i][j], (resize_width, resize_height))
                    # CONVERT IMAGES TO SAME CHANNEL
                    img_arr[i][j] = self.convert_to_bgr(img_arr[i][j])

            hor = []
            for i in range(0, x):
                hor.append(np.hstack(img_arr[i]))
            ver = np.vstack(hor)
        else:

            resize_width = int(img_arr[0].shape[1] * scale / x)
            resize_height = int(img_arr[0].shape[0] * scale / x)

            for i in range(x):
                # CONVERT IMAGES TO SAME SIZE - IF ALREADY SAME SIZE, NOTHING CHANGES
                img_arr[i] = cv2.resize(img_arr[i], (resize_width, resize_height))
                # CONVERT IMAGES TO SAME CHANNEL
                img_arr[i] = self.convert_to_bgr(img_arr[i])

            hor = np.hstack(img_arr)
            ver = hor
        return ver

    @staticmethod
    def write_text(img, text, org):
        """
        Writes text to an image
        :param img: Image to draw
        :param text: Text to display
        :param org: Position of the text
        :return: None
        """
        cv2.putText(
            img=img,
            text=text,
            org=org,
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.6,
            color=(0, 255, 0),
            thickness=1
        )
