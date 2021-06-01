import time

import cv2

from bots.image_processing_bot.ImageProcessingBotService import ImageProcessingBotService
from utils import constants, game_constants


class NavigationBot:

    def __init__(self):
        self.image_processing_bot = ImageProcessingBotService()
        self.mini_map_rect = game_constants.LOCATIONS['mini_map']
        self.blank_image = self.image_processing_bot.get_blank_image()

    def get_mini_map(self):
        img = self.image_processing_bot.screenshot()
        return self.image_processing_bot.get_img_segment(img, self.mini_map_rect)

    def get_mini_map_facilities(self):
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

        while cv2.waitKey(1) or 0xFF == ord('q'):
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

            self.image_processing_bot.draw_contours(eroded, contour, contour_min_area, contour_max_area)

            img_stack = [[img, blurred],
                         [contrast_adjusted, self.blank_image],
                         [masked, grayed],
                         [canny, dilated],
                         [eroded, contour]]

            stacked = self.image_processing_bot.stack_images(img_stack, 3)

            cv2.imshow('Crafting Facilities', stacked)
        cv2.destroyAllWindows()


nav_bot = NavigationBot()

nav_bot.get_mini_map_facilities()