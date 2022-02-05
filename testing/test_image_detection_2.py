import cv2

from bots.image_processing_bot.ImageProcessingBotService import ImageProcessingBotService
from bots.navigation_bot.NavigationBotService import NavigationBotService

nav_bot = NavigationBotService()
img_bot = ImageProcessingBotService()

img_bot.create_gaussian_blur_trackbar(window_name='Trackbar')
img_bot.create_brightness_trackbar(window_name='Trackbar')
img_bot.create_contrast_trackbar(window_name='Trackbar')
img_bot.create_hsv_trackbar(window_name='Trackbar')
img_bot.create_canny_trackbar(120, 120, 'Trackbar')
img_bot.create_dilation_trackbar(window_name='Trackbar')
img_bot.create_erosion_trackbar(window_name='Trackbar')
img_bot.create_contour_trackbar(window_name='Trackbar', default_max_area=25000)
img_bot.create_rectangle_trackbar(window_name='Trackbar')

while cv2.waitKey(1) or 0xFF == ord('q'):
    blur_kernel, blur_sigma_x = img_bot.get_gaussian_blur_trackbar_values('Trackbar')
    brightness = img_bot.get_brightness_trackbar_value('Trackbar')
    contrast = img_bot.get_contrast_trackbar_value('Trackbar')
    hsv_lower, hsv_upper = img_bot.get_hsv_trackbar_values('Trackbar')
    canny_thresh_1, canny_thresh_2 = img_bot.get_canny_trackbar_values('Trackbar')
    dilation_kernel, dilation_iterations = img_bot.get_dilation_trackbar_values('Trackbar')
    erosion_kernel, erosion_iterations = img_bot.get_erosion_trackbar_values('Trackbar')
    contour_min_area, contour_max_area = img_bot.get_contour_trackbar_values('Trackbar')

    img = nav_bot.get_mini_map_cropped()
    img = img_bot.convert_to_bgr(img)
    contour = img.copy()

    blurred = img_bot.gaussian_blur(img, blur_kernel, blur_sigma_x)
    brightness_adjusted = img_bot.adjust_brightness(blurred, brightness)
    contrast_adjusted = img_bot.adjust_contrast(brightness_adjusted, contrast)
    masked = img_bot.mask(contrast_adjusted, hsv_lower, hsv_upper)
    grayed = img_bot.gray(masked)
    canny = img_bot.canny(grayed, canny_thresh_1, canny_thresh_2)
    dilated = img_bot.dilate(canny, dilation_kernel, dilation_iterations)
    eroded = img_bot.erode(dilated, erosion_kernel, erosion_iterations)

    img_bot.find_and_draw_contours(eroded, contour, contour_min_area, contour_max_area)

    img_stack = [[img, blurred],
                 [brightness_adjusted, contrast_adjusted],
                 [masked, grayed],
                 [canny, dilated],
                 [eroded, contour]]

    stacked = img_bot.stack_images(img_stack, 6)

    cv2.imshow("Stacked", stacked)

cv2.destroyAllWindows()