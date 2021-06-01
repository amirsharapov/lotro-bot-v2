from time import time

import cv2
import cv2 as cv

from bots.image_processing_bot.ImageProcessingBotService import ImageProcessingBotService
from utils import game_constants

bot = ImageProcessingBotService()


def main():
    loop_time = time()

    cv2.namedWindow('Trackbar')
    cv2.resizeWindow('Trackbar', 800, 800)

    blank = bot.get_blank_image()

    # SETUP TRACKBARS
    bot.create_gaussian_blur_trackbar(window_name='Trackbar')
    bot.create_brightness_trackbar(window_name='Trackbar')
    bot.create_contrast_trackbar(window_name='Trackbar')
    bot.create_hsv_trackbar(window_name='Trackbar')
    bot.create_canny_trackbar(120, 120, 'Trackbar')
    bot.create_dilation_trackbar(window_name='Trackbar')
    bot.create_erosion_trackbar(window_name='Trackbar')
    bot.create_contour_trackbar(window_name='Trackbar')
    bot.create_rectangle_trackbar(window_name='Trackbar')

    portrait_rect = game_constants.LOCATIONS['portrait']
    mini_map_rect = game_constants.LOCATIONS['mini_map']
    chat_rect = game_constants.LOCATIONS['chat']
    skill_bar_rect = game_constants.LOCATIONS['skill_bar']

    while True:

        # GET TRACKBAR VALUES
        blur_kernel, blur_sigma_x = bot.get_gaussian_blur_trackbar_values('Trackbar')
        brightness = bot.get_brightness_trackbar_value('Trackbar')
        contrast = bot.get_contrast_trackbar_value('Trackbar')
        hsv_lower, hsv_upper = bot.get_hsv_trackbar_values('Trackbar')
        canny_thresh_1, canny_thresh_2 = bot.get_canny_trackbar_values('Trackbar')
        dilation_kernel, dilation_iterations = bot.get_dilation_trackbar_values('Trackbar')
        erosion_kernel, erosion_iterations = bot.get_erosion_trackbar_values('Trackbar')
        contour_min_area, contour_max_area = bot.get_contour_trackbar_values('Trackbar')

        img = bot.screenshot()
        img = bot.convert_to_bgr(img)

        bot.draw_rectangle(img, portrait_rect, (0, 0, 0), -1)  # hide character portrait
        bot.draw_rectangle(img, mini_map_rect, (0, 0, 0), -1)  # hide mini map
        bot.draw_rectangle(img, chat_rect, (0, 0, 0), -1)  # hide chat channels
        bot.draw_rectangle(img, skill_bar_rect, (0, 0, 0), -1)  # hide main skill bar

        contour = img.copy()

        # PROCESS MAIN SCREEN
        blurred = bot.gaussian_blur(img, blur_kernel, blur_sigma_x)
        brightness_adjusted = bot.adjust_brightness(blurred, brightness)
        contrast_adjusted = bot.adjust_contrast(brightness_adjusted, contrast)
        masked = bot.mask(contrast_adjusted, hsv_lower, hsv_upper)
        grayed = bot.gray(masked)
        canny = bot.canny(grayed, canny_thresh_1, canny_thresh_2)
        dilated = bot.dilate(canny, dilation_kernel, dilation_iterations)
        eroded = bot.erode(dilated, erosion_kernel, erosion_iterations)

        # DRAW CONTOURS
        bot.draw_contours(eroded, contour, contour_min_area, contour_max_area)

        # STACK IMAGES
        img_stack = [[img, blurred],
                     [brightness_adjusted, contrast_adjusted],
                     [masked, grayed],
                     [canny, eroded],
                     [dilated, contour]]
        stacked = bot.stack_images(img_stack, 1)

        cv.imshow("Object Detection", stacked)

        print(f"FPS: {1 / (time() - loop_time)}")
        loop_time = time()

        # SET BREAK
        if cv.waitKey(1) & 0xFF == ord('q'):
            cv.destroyAllWindows()
            break


main()
