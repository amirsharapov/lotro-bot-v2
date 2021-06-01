import cv2
import cv2 as cv
import numpy as np

from bots.detection_bot.DetectionBotService import DetectionBotService
from bots.image_processing_bot.ImageProcessingBotService import ImageProcessingBotService

image_processing_bot = ImageProcessingBotService()
detection_bot = DetectionBotService()

ix, iy, k = 200, 200, 1


def on_mouse(event, x, y, flag, param):
    global ix, iy, k
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'left button clicked{x}, {y}')
        ix, iy = x, y
        k = -1


image_processing_bot.create_window('image')
cv2.setMouseCallback('image', on_mouse)

prev_frame = None

while cv.waitKey(1):

    img = image_processing_bot.screenshot()
    img = image_processing_bot.convert_to_bgr(img)

    cv2.imshow('image', img)

    if cv2.waitKey(1) and 0xFF == ord('q') or k == -1:
        old_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.destroyAllWindows()
        break

old_pts = np.array([[ix, iy]], dtype='float32').reshape(-1, 1, 2)
mask = np.zeros_like(img)

mask = np.zeros_like(img)

while True:

    img = image_processing_bot.screenshot()
    img = image_processing_bot.convert_to_bgr(img)

    new_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    new_pts, status, err = cv2.calcOpticalFlowPyrLK(
        new_gray,
        old_gray,
        None,
        maxLevel=1,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 0.08)
    )

    if cv2.waitKey(1) and 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
