import datetime
import threading
import time

import cv2

from bots.detection_bot.DetectionBotService import DetectionBotService
from bots.image_processing_bot.ImageProcessingBotService import ImageProcessingBotService

detection_bot = DetectionBotService()
image_processing_bot = ImageProcessingBotService()

loop_time = time.time()

while cv2.waitKey(1):

    img = image_processing_bot.screenshot()

    # DETECT STUFF
    thread1 = threading.Thread(target=detection_bot.detect_mini_map_crafting_facilities, args=[img])
    thread2 = threading.Thread(target=detection_bot.detect_mini_map_character_marker, args=[img])
    thread3 = threading.Thread(target=detection_bot.detect_yellow_nameplates, args=[img])
    thread4 = threading.Thread(target=detection_bot.detect_white_nameplates, args=[img])

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

    img = image_processing_bot.resize_image(img, 0.9)
    cv2.imshow('img', img)

    print(f"FPS: {1 / (time.time() - loop_time)}")
    loop_time = time.time()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
