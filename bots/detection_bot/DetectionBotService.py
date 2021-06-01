import datetime
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

    def get_mini_map(self):
        img = self.image_processing_bot.screenshot()
        return self.image_processing_bot.get_img_segment(img, self.mini_map_rect)

    def get_mini_map_cropped(self):
        img = self.get_mini_map()
        return self.image_processing_bot.get_img_segment(img, self.mini_map_cropped_rect)

    def detect_yellow_nameplates(self):
        detection_obj_values = game_constants.RECOGNITION['nameplates']['colors']['yellow']

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

        while cv2.waitKey(1):

            img = self.image_processing_bot.screenshot()
            img = self.image_processing_bot.convert_to_bgr(img)

            self.image_processing_bot.draw_rectangle(img, self.portrait_rect, (0, 0, 0), -1)  # hide character portrait
            self.image_processing_bot.draw_rectangle(img, self.mini_map_rect, (0, 0, 0), -1)  # hide mini map
            self.image_processing_bot.draw_rectangle(img, self.chat_rect, (0, 0, 0), -1)  # hide chat channels
            self.image_processing_bot.draw_rectangle(img, self.skill_bar_rect, (0, 0, 0), -1)  # hide main skill bar

            img_contour = img.copy()

            blurred = self.image_processing_bot.gaussian_blur(img, gaussian_kernel, gaussian_sigma_x)
            masked = self.image_processing_bot.mask(blurred, lower_hsv, upper_hsv)
            grayed = self.image_processing_bot.gray(masked)
            canny = self.image_processing_bot.canny(grayed, threshold_1, threshold_2)
            dilated = self.image_processing_bot.dilate(canny, dilation_kernel, dilation_iterations)
            rects = self.image_processing_bot.draw_contours(dilated, img_contour, contour_min_area, contour_max_area)

            img_stack = [img_contour]

            stacked = self.image_processing_bot.stack_images(img_stack, .45)
            cv2.imshow('yellow_nameplates', stacked)

            for rect in rects:
                segment = self.image_processing_bot.get_img_segment(img, rect)
                print(segment)
                self.image_processing_bot.save_as_training_data(segment)

            time.sleep(.2)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def detect_white_nameplates(self):

        detection_obj_values = game_constants.RECOGNITION['nameplates']['colors']['white']

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

        while cv2.waitKey(1):

            img = self.image_processing_bot.screenshot()
            img = self.image_processing_bot.convert_to_bgr(img)

            self.image_processing_bot.draw_rectangle(img, self.portrait_rect, (0, 0, 0), -1)  # hide character portrait
            self.image_processing_bot.draw_rectangle(img, self.mini_map_rect, (0, 0, 0), -1)  # hide mini map
            self.image_processing_bot.draw_rectangle(img, self.chat_rect, (0, 0, 0), -1)  # hide chat channels
            self.image_processing_bot.draw_rectangle(img, self.skill_bar_rect, (0, 0, 0), -1)  # hide main skill bar

            img_contour = img.copy()

            blurred = self.image_processing_bot.gaussian_blur(img, gaussian_kernel, gaussian_sigma_x)
            brightness_adjusted = self.image_processing_bot.adjust_brightness(blurred, brightness)
            contrast_adjusted = self.image_processing_bot.adjust_contrast(brightness_adjusted, contrast)
            masked = self.image_processing_bot.mask(contrast_adjusted, lower_hsv, upper_hsv)
            grayed = self.image_processing_bot.gray(masked)
            canny = self.image_processing_bot.canny(grayed, threshold_1, threshold_2)
            dilated = self.image_processing_bot.dilate(canny, dilation_kernel, dilation_iterations)
            eroded = self.image_processing_bot.erode(dilated, erosion_kernel, erosion_iterations)
            self.image_processing_bot.draw_contours(eroded, img_contour, contour_min_area, contour_max_area)

            stacked = self.image_processing_bot.stack_images([img_contour], .45)
            cv2.imshow('white_nameplates', stacked)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def detect_mini_map_facilities(self):
        blank_image = self.image_processing_bot.get_blank_image()
        detection_obj_values = game_constants.RECOGNITION['objects']['mini_map']['crafting_facility']

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

        while cv2.waitKey(1):
            img = self.get_mini_map()
            img = self.image_processing_bot.convert_to_bgr(img)
            contour = img.copy()

            blurred = self.image_processing_bot.gaussian_blur(img, gaussian_blur_kernel, gaussian_blur_sigma_x)
            contrast_adjusted = self.image_processing_bot.adjust_contrast(blurred, contrast)
            masked = self.image_processing_bot.mask(contrast_adjusted, lower_hsv, upper_hsv)
            grayed = self.image_processing_bot.gray(masked)
            canny = self.image_processing_bot.canny(grayed, canny_threshold_1, canny_threshold_2)
            dilated = self.image_processing_bot.dilate(canny, dilation_kernel, dilation_iterations)
            eroded = self.image_processing_bot.erode(dilated, erosion_kernel, erosion_iterations)

            rects = self.image_processing_bot.draw_contours(eroded, contour, contour_min_area, contour_max_area)

            img_stack = [[img, blurred],
                         [contrast_adjusted, blank_image],
                         [masked, grayed],
                         [canny, dilated],
                         [eroded, contour]]

            stacked = self.image_processing_bot.stack_images([contour], 1.5)
            cv2.imshow('crafting_facilities', stacked)

            for rect in rects:
                x1, y1, _, _ = self.mini_map_rect
                x2, y2, _, _ = self.mini_map_cropped_rect
                x3, y3, w, h = rect

                real_rect = (x1 + x2 + x3,
                             y1 + y2 + y3,
                             w, h)
                print(real_rect)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def detect_mini_map_character_marker(self):
        blank_image = self.image_processing_bot.get_blank_image()
        detection_obj_values = game_constants.RECOGNITION['objects']['mini_map']['character_marker']

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

        while cv2.waitKey(1):
            img = self.get_mini_map_cropped()
            img = self.image_processing_bot.convert_to_bgr(img)
            contour = img.copy()

            blurred = self.image_processing_bot.gaussian_blur(img, gaussian_blur_kernel, gaussian_blur_sigma_x)
            brightness_adjusted = self.image_processing_bot.adjust_contrast(blurred, brightness)
            masked = self.image_processing_bot.mask(brightness_adjusted, lower_hsv, upper_hsv)
            grayed = self.image_processing_bot.gray(masked)
            canny = self.image_processing_bot.canny(grayed, canny_threshold_1, canny_threshold_2)
            dilated = self.image_processing_bot.dilate(canny, dilation_kernel, dilation_iterations)
            eroded = self.image_processing_bot.erode(dilated, erosion_kernel, erosion_iterations)

            self.image_processing_bot.draw_contours(eroded, contour, contour_min_area, contour_max_area)

            img_stack = [[img, blurred],
                         [brightness_adjusted, blank_image],
                         [masked, grayed],
                         [canny, dilated],
                         [eroded, contour]]

            stacked = self.image_processing_bot.stack_images([contour], 3)
            cv2.imshow('character_marker', stacked)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
