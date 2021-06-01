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

        # PROCESSING
        gaussian_kernel = game_constants.YELLOW_COLOR['gaussian_blur']['kernel']
        gaussian_sigma_x = game_constants.YELLOW_COLOR['gaussian_blur']['sigma_x']
        threshold_1 = game_constants.YELLOW_COLOR['canny_threshold']['threshold_1']
        threshold_2 = game_constants.YELLOW_COLOR['canny_threshold']['threshold_2']
        lower_hsv = (game_constants.YELLOW_COLOR['hsv_mask_range']['lower_hue'],
                     game_constants.YELLOW_COLOR['hsv_mask_range']['lower_saturation'],
                     game_constants.YELLOW_COLOR['hsv_mask_range']['lower_value'])
        upper_hsv = (game_constants.YELLOW_COLOR['hsv_mask_range']['upper_hue'],
                     game_constants.YELLOW_COLOR['hsv_mask_range']['upper_saturation'],
                     game_constants.YELLOW_COLOR['hsv_mask_range']['upper_value'])
        contour_min_area = game_constants.YELLOW_COLOR['contour_area_range']['min_area']
        contour_max_area = game_constants.YELLOW_COLOR['contour_area_range']['max_area']
        dilation_kernel = game_constants.YELLOW_COLOR['dilation']['kernel']
        dilation_iterations = game_constants.YELLOW_COLOR['dilation']['iterations']

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
        gaussian_kernel = game_constants.WHITE_COLOR['gaussian_blur']['kernel']
        gaussian_sigma_x = game_constants.WHITE_COLOR['gaussian_blur']['sigma_x']
        brightness = game_constants.WHITE_COLOR['brightness']['level']
        contrast = game_constants.WHITE_COLOR['contrast']['level']
        threshold_1 = game_constants.WHITE_COLOR['canny_threshold']['threshold_1']
        threshold_2 = game_constants.WHITE_COLOR['canny_threshold']['threshold_2']
        lower_hsv = (game_constants.WHITE_COLOR['hsv_mask_range']['lower_hue'],
                     game_constants.WHITE_COLOR['hsv_mask_range']['lower_saturation'],
                     game_constants.WHITE_COLOR['hsv_mask_range']['lower_value'])
        upper_hsv = (game_constants.WHITE_COLOR['hsv_mask_range']['upper_hue'],
                     game_constants.WHITE_COLOR['hsv_mask_range']['upper_saturation'],
                     game_constants.WHITE_COLOR['hsv_mask_range']['upper_value'])
        contour_min_area = game_constants.WHITE_COLOR['contour_area_range']['min_area']
        contour_max_area = game_constants.WHITE_COLOR['contour_area_range']['max_area']
        dilation_kernel = game_constants.WHITE_COLOR['dilation']['kernel']
        dilation_iterations = game_constants.WHITE_COLOR['dilation']['iterations']
        erosion_kernel = game_constants.WHITE_COLOR['erosion']['kernel']
        erosion_iterations = game_constants.WHITE_COLOR['erosion']['iterations']

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

# bot.detect_white_colors()
bot.detect_yellow_colors()
