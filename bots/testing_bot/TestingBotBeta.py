import random
import time

import cv2
import cv2 as cv
import numpy as np

from bots.image_detection_bot.ImageDetectionBotService import ImageDetectionBotService
from bots.image_processing_bot.ImageProcessingBotService import ImageProcessingBotService

image_processing_bot = ImageProcessingBotService()
image_detection_bot = ImageDetectionBotService()


def calculate_direction(difference_param, direction_param):
    if difference_param is None:
        return None
    if difference_param[0] > -0.001:
        dir_a = 'west'
    elif difference_param[0] < 0.001:
        dir_a = 'east'
    else:
        dir_a = None

    if difference_param[1] > -0.001:
        dir_b = 'north'
    elif difference_param[1] < 0.001:
        dir_b = 'south'
    else:
        dir_b = None

    if dir_a and dir_b is not None:
        if dir_a is None:
            direction_param = dir_b
        elif dir_b is None:
            direction_param = dir_a
        else:
            direction_param = f'{dir_a}{dir_b}'
    else:
        direction_param = None

    return direction_param


direction = 'None'

img = image_detection_bot.get_mini_map_cropped()

height = img.shape[0]
width = img.shape[1]

x = random.randint(30, width - 30)
y = random.randint(30, height - 30)

gray = image_processing_bot.gray(img)

pts = np.array([[x, y]], dtype='float32').reshape(-1, 1, 2)
mask = np.zeros_like(img)

while True:
    time.sleep(.4)
    new_img = image_detection_bot.get_mini_map_cropped()
    new_gray = image_processing_bot.gray(new_img)

    new_pts, status, err = cv2.calcOpticalFlowPyrLK(
        gray,
        new_gray,
        pts,
        None,
        maxLevel=1,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 9, 0.08)
    )
    difference = (new_pts.ravel()[0] - pts.ravel()[0], new_pts.ravel()[1] - pts.ravel()[1])
    if np.all(difference == [0., 0.]):
        difference = None
    print(difference)
    direction = calculate_direction(difference, direction)

    if direction is not None:
        print(f'Direction: {direction}')
    cv2.circle(mask, (int(new_pts.ravel()[0]), int(new_pts.ravel()[1])), 2, (0, 255, 0), 1)

    cv.imshow('window', mask)

    gray = new_gray.copy()
    pts = new_pts.copy()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
