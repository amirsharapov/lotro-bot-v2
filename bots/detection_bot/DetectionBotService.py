import cv2

from bots.image_processing_bot.ImageProcessingBotService import ImageProcessingBotService
from utils import game_constants


class IdentificationBotService:

    def __init__(self):
        self.loop_time = 0
        self.imaging_bot = ImageProcessingBotService()
        self.portrait_rect = game_constants.LOCATIONS['portrait']
        self.mini_map_rect = game_constants.LOCATIONS['mini_map']
        self.chat_rect = game_constants.LOCATIONS['chat']
        self.skill_bar_rect = game_constants.LOCATIONS['skill_bar']

    def detect_yellow_colors(self):
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

        while cv2.waitKey(1) or 0xFF == ord('q'):

            img = self.imaging_bot.screenshot()
            img = self.imaging_bot.convert_to_bgr(img)

            self.imaging_bot.draw_rectangle(img, self.portrait_rect, (0, 0, 0), -1)  # hide character portrait
            self.imaging_bot.draw_rectangle(img, self.mini_map_rect, (0, 0, 0), -1)  # hide mini map
            self.imaging_bot.draw_rectangle(img, self.chat_rect, (0, 0, 0), -1)  # hide chat channels
            self.imaging_bot.draw_rectangle(img, self.skill_bar_rect, (0, 0, 0), -1)  # hide main skill bar

            img_contour = img.copy()

            blurred = self.imaging_bot.gaussian_blur(img, gaussian_kernel, gaussian_sigma_x)
            masked = self.imaging_bot.mask(blurred, lower_hsv, upper_hsv)
            grayed = self.imaging_bot.gray(masked)
            canny = self.imaging_bot.canny(grayed, threshold_1, threshold_2)
            dilated = self.imaging_bot.dilate(canny, dilation_kernel, dilation_iterations)
            self.imaging_bot.draw_contours(dilated, img_contour, contour_min_area, contour_max_area)

            img_stack = [img_contour]

            stacked = self.imaging_bot.stack_images(img_stack, .8)
            cv2.imshow('NPC Identification', stacked)

        cv2.destroyAllWindows()

    def detect_white_colors(self):
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

        while cv2.waitKey(1) or 0xFF == ord('q'):

            img = self.imaging_bot.screenshot()
            img_contour = img.copy()

            blurred = self.imaging_bot.gaussian_blur(img, gaussian_kernel, gaussian_sigma_x)
            brightness_adjusted = self.imaging_bot.adjust_brightness(blurred, brightness)
            contrast_adjusted = self.imaging_bot.adjust_contrast(brightness_adjusted, contrast)
            masked = self.imaging_bot.mask(contrast_adjusted, lower_hsv, upper_hsv)
            grayed = self.imaging_bot.gray(masked)
            canny = self.imaging_bot.canny(grayed, threshold_1, threshold_2)
            dilated = self.imaging_bot.dilate(canny, dilation_kernel, dilation_iterations)
            eroded = self.imaging_bot.erode(dilated, erosion_kernel, erosion_iterations)
            self.imaging_bot.draw_contours(eroded, img_contour, contour_min_area, contour_max_area)

            stacked = self.imaging_bot.stack_images([img_contour], .8)
            cv2.imshow('NPC Identification', stacked)

        cv2.destroyAllWindows()


bot = IdentificationBotService()

bot.detect_white_colors()
# bot.detect_yellow_colors()
