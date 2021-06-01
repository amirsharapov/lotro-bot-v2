import time

import cv2

from bots.image_processing_bot.ImageProcessingBotService import ImageProcessingBotService
from utils import game_constants


class DetectionBotService:

    def __init__(self):
        self.loop_time = 0
        # External bots
        self.image_processing_bot = ImageProcessingBotService()
        # Rectangles
        self.portrait_rect = game_constants.LOCATIONS['portrait']
        self.mini_map_rect = game_constants.LOCATIONS['mini_map']
        self.mini_map_cropped_rect = game_constants.LOCATIONS['mini_map_cropped']
        self.chat_rect = game_constants.LOCATIONS['chat']
        self.skill_bar_rect = game_constants.LOCATIONS['skill_bar']

    def get_mini_map(self, img=None):
        if img is None:
            img = self.image_processing_bot.screenshot()
        else:
            img = img.copy()
        return self.image_processing_bot.get_img_segment(img, self.mini_map_rect)

    def get_mini_map_cropped(self, img=None):
        img = self.get_mini_map(img)
        return self.image_processing_bot.get_img_segment(img, self.mini_map_cropped_rect)

    def detect_yellow_nameplates(self, contour_canvas=None, economic=True):
        detection_obj_values = game_constants.RECOGNITION['nameplates']['colors']['yellow']

        # SETUP IMAGE PROCESSING VALUES
        gaussian_kernel = detection_obj_values['gaussian_blur']['kernel']
        gaussian_sigma_x = detection_obj_values['gaussian_blur']['sigma_x']
        threshold_1 = detection_obj_values['canny']['threshold_1']
        threshold_2 = detection_obj_values['canny']['threshold_2']
        lower_hsv = (detection_obj_values['mask']['lower_hue'],
                     detection_obj_values['mask']['lower_saturation'],
                     detection_obj_values['mask']['lower_value'])
        upper_hsv = (detection_obj_values['mask']['upper_hue'],
                     detection_obj_values['mask']['upper_saturation'],
                     detection_obj_values['mask']['upper_value'])
        contour_min_area = detection_obj_values['contour']['min_area']
        contour_max_area = detection_obj_values['contour']['max_area']
        dilation_kernel = detection_obj_values['dilation']['kernel']
        dilation_iterations = detection_obj_values['dilation']['iterations']

        if contour_canvas is not None and economic:
            img = contour_canvas.copy()
        else:
            img = self.image_processing_bot.screenshot()
        img = self.image_processing_bot.convert_to_bgr(img)

        self.image_processing_bot.draw_rectangle(img, self.portrait_rect, (0, 0, 0), -1)  # hide character portrait
        self.image_processing_bot.draw_rectangle(img, self.mini_map_rect, (0, 0, 0), -1)  # hide mini map
        self.image_processing_bot.draw_rectangle(img, self.chat_rect, (0, 0, 0), -1)  # hide chat channels
        self.image_processing_bot.draw_rectangle(img, self.skill_bar_rect, (0, 0, 0), -1)  # hide main skill bar

        if contour_canvas is None:
            contour_canvas = img.copy()

        blurred = self.image_processing_bot.gaussian_blur(img, gaussian_kernel, gaussian_sigma_x)
        masked = self.image_processing_bot.mask(blurred, lower_hsv, upper_hsv)
        grayed = self.image_processing_bot.gray(masked)
        canny = self.image_processing_bot.canny(grayed, threshold_1, threshold_2)
        dilated = self.image_processing_bot.dilate(canny, dilation_kernel, dilation_iterations)

        self.image_processing_bot.find_and_draw_contours(
            dilated,
            contour_canvas,
            contour_min_area,
            contour_max_area
        )

    def detect_white_nameplates(self, contour_canvas=None, economic=True):
        detection_obj_values = game_constants.RECOGNITION['nameplates']['colors']['white']

        # GET IMAGE PROCESSING VALUES
        gaussian_kernel = detection_obj_values['gaussian_blur']['kernel']
        gaussian_sigma_x = detection_obj_values['gaussian_blur']['sigma_x']
        brightness = detection_obj_values['brightness']['level']
        contrast = detection_obj_values['contrast']['level']
        threshold_1 = detection_obj_values['canny']['threshold_1']
        threshold_2 = detection_obj_values['canny']['threshold_2']
        lower_hsv = (detection_obj_values['mask']['lower_hue'],
                     detection_obj_values['mask']['lower_saturation'],
                     detection_obj_values['mask']['lower_value'])
        upper_hsv = (detection_obj_values['mask']['upper_hue'],
                     detection_obj_values['mask']['upper_saturation'],
                     detection_obj_values['mask']['upper_value'])
        contour_min_area = detection_obj_values['contour']['min_area']
        contour_max_area = detection_obj_values['contour']['max_area']
        dilation_kernel = detection_obj_values['dilation']['kernel']
        dilation_iterations = detection_obj_values['dilation']['iterations']
        erosion_kernel = detection_obj_values['erosion']['kernel']
        erosion_iterations = detection_obj_values['erosion']['iterations']

        # SETUP IMAGES FOR PROCESSING
        if contour_canvas is not None and economic:
            img = contour_canvas.copy()
        else:
            img = self.image_processing_bot.screenshot()
        img = self.image_processing_bot.convert_to_bgr(img)

        self.image_processing_bot.draw_rectangle(img, self.portrait_rect, (0, 0, 0), -1)  # hide character portrait
        self.image_processing_bot.draw_rectangle(img, self.mini_map_rect, (0, 0, 0), -1)  # hide mini map
        self.image_processing_bot.draw_rectangle(img, self.chat_rect, (0, 0, 0), -1)  # hide chat channels
        self.image_processing_bot.draw_rectangle(img, self.skill_bar_rect, (0, 0, 0), -1)  # hide main skill bar

        if contour_canvas is None:
            contour_canvas = img.copy()

        # PROCESS IMAGES
        blurred = self.image_processing_bot.gaussian_blur(img, gaussian_kernel, gaussian_sigma_x)
        brightness_adjusted = self.image_processing_bot.adjust_brightness(blurred, brightness)
        contrast_adjusted = self.image_processing_bot.adjust_contrast(brightness_adjusted, contrast)
        masked = self.image_processing_bot.mask(contrast_adjusted, lower_hsv, upper_hsv)
        grayed = self.image_processing_bot.gray(masked)
        canny = self.image_processing_bot.canny(grayed, threshold_1, threshold_2)
        dilated = self.image_processing_bot.dilate(canny, dilation_kernel, dilation_iterations)
        eroded = self.image_processing_bot.erode(dilated, erosion_kernel, erosion_iterations)

        # IMAGE HAS NO OFFSET
        self.image_processing_bot.find_and_draw_contours(
            eroded,
            contour_canvas,
            contour_min_area,
            contour_max_area
        )

    def detect_mini_map_crafting_facilities(self, contour_canvas=None):
        """
        Detects crafting facilities on the mini map
        :param contour_canvas: Image to draw canvas on. DO NOT supply an image smaller than the full size of the screen
        :return: None
        """
        detection_obj_values = game_constants.RECOGNITION['objects']['mini_map']['crafting_facility']

        # GET IMAGE PROCESSING VALUES
        gaussian_blur_kernel = detection_obj_values['gaussian_blur']['kernel']
        gaussian_blur_sigma_x = detection_obj_values['gaussian_blur']['sigma_x']
        contrast = detection_obj_values['brightness']['value']
        lower_hsv = (detection_obj_values['mask']['lower_hue'],
                     detection_obj_values['mask']['lower_saturation'],
                     detection_obj_values['mask']['lower_value'])
        upper_hsv = (detection_obj_values['mask']['upper_hue'],
                     detection_obj_values['mask']['upper_saturation'],
                     detection_obj_values['mask']['upper_value'])
        canny_threshold_1 = detection_obj_values['canny']['threshold_1']
        canny_threshold_2 = detection_obj_values['canny']['threshold_2']
        dilation_kernel = detection_obj_values['dilation']['kernel']
        dilation_iterations = detection_obj_values['dilation']['iterations']
        erosion_kernel = detection_obj_values['erosion']['kernel']
        erosion_iterations = detection_obj_values['erosion']['iterations']
        contour_min_area = detection_obj_values['contour']['min_area']
        contour_max_area = detection_obj_values['contour']['max_area']

        # SETUP IMAGES FOR PROCESSING
        mini_map = self.get_mini_map(contour_canvas)
        mini_map = self.image_processing_bot.convert_to_bgr(mini_map)
        if contour_canvas is None:
            contour_canvas = mini_map.copy()

        # PROCESS IMAGE
        blurred = self.image_processing_bot.gaussian_blur(mini_map, gaussian_blur_kernel, gaussian_blur_sigma_x)
        contrast_adjusted = self.image_processing_bot.adjust_contrast(blurred, contrast)
        masked = self.image_processing_bot.mask(contrast_adjusted, lower_hsv, upper_hsv)
        grayed = self.image_processing_bot.gray(masked)
        canny = self.image_processing_bot.canny(grayed, canny_threshold_1, canny_threshold_2)
        dilated = self.image_processing_bot.dilate(canny, dilation_kernel, dilation_iterations)
        eroded = self.image_processing_bot.erode(dilated, erosion_kernel, erosion_iterations)

        # GET IMAGE OFFSET
        x1, y1, _, _ = self.mini_map_rect
        offset = (x1, y1)

        # IF CANVAS IS PROVIDED
        if contour_canvas is None:
            self.image_processing_bot.find_and_draw_contours(
                eroded,
                contour_canvas,
                contour_min_area,
                contour_max_area
            )
        # IF CANVAS IS NOT PROVIDED
        else:
            self.image_processing_bot.find_and_draw_contours(
                eroded,
                contour_canvas,
                contour_min_area,
                contour_max_area,
                drawing_offset=offset
            )

    def detect_mini_map_character_marker(self, contour_canvas=None, economic=True):
        detection_obj_values = game_constants.RECOGNITION['objects']['mini_map']['character_marker']

        # GET IMAGE PROCESSING VALUES
        gaussian_blur_kernel = detection_obj_values['gaussian_blur']['kernel']
        gaussian_blur_sigma_x = detection_obj_values['gaussian_blur']['sigma_x']
        brightness = detection_obj_values['brightness']['level']
        lower_hsv = (detection_obj_values['mask']['lower_hue'],
                     detection_obj_values['mask']['lower_saturation'],
                     detection_obj_values['mask']['lower_value'])
        upper_hsv = (detection_obj_values['mask']['upper_hue'],
                     detection_obj_values['mask']['upper_saturation'],
                     detection_obj_values['mask']['upper_value'])
        canny_threshold_1 = detection_obj_values['canny']['threshold_1']
        canny_threshold_2 = detection_obj_values['canny']['threshold_2']
        dilation_kernel = detection_obj_values['dilation']['kernel']
        dilation_iterations = detection_obj_values['dilation']['iterations']
        erosion_kernel = detection_obj_values['erosion']['kernel']
        erosion_iterations = detection_obj_values['erosion']['iterations']
        contour_min_area = detection_obj_values['contour']['min_area']
        contour_max_area = detection_obj_values['contour']['max_area']

        # SETUP IMAGES FOR PROCESSING
        mini_map = self.get_mini_map_cropped(contour_canvas)
        mini_map = self.image_processing_bot.convert_to_bgr(mini_map)
        if contour_canvas is None:
            contour_canvas = mini_map.copy()

        # PROCESS IMAGE
        blurred = self.image_processing_bot.gaussian_blur(mini_map, gaussian_blur_kernel, gaussian_blur_sigma_x)
        brightness_adjusted = self.image_processing_bot.adjust_contrast(blurred, brightness)
        masked = self.image_processing_bot.mask(brightness_adjusted, lower_hsv, upper_hsv)
        grayed = self.image_processing_bot.gray(masked)
        canny = self.image_processing_bot.canny(grayed, canny_threshold_1, canny_threshold_2)
        dilated = self.image_processing_bot.dilate(canny, dilation_kernel, dilation_iterations)
        eroded = self.image_processing_bot.erode(dilated, erosion_kernel, erosion_iterations)

        # GET IMAGE OFFSET
        x1, y1, _, _ = self.mini_map_rect
        x2, y2, _, _ = self.mini_map_cropped_rect
        offset = (x1 + x2, y1 + y2)

        # IF CANVAS IS PROVIDED
        if contour_canvas is None:
            self.image_processing_bot.find_and_draw_contours(
                eroded,
                contour_canvas,
                contour_min_area,
                contour_max_area
            )
        # IF CANVAS IS NOT PROVIDED
        else:
            self.image_processing_bot.find_and_draw_contours(
                eroded,
                contour_canvas,
                contour_min_area,
                contour_max_area,
                drawing_offset=offset
            )


