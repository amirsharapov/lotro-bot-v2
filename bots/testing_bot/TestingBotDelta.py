import cv2
import numpy as np

from bots.image_processing_bot.ImageProcessingBotService import ImageProcessingBotService

bot = ImageProcessingBotService()

img = np.zeros((100, 100, 3), np.uint8)
img2 = np.zeros((100, 100, 3), np.uint8)

cv2.circle(img, (50, 50), 50, (255, 255, 255), -1)
cv2.circle(img2, (50, 50), 25, (0, 255, 0), -1)

img3 = cv2.bitwise_xor(img, img2)

for i in range(len(img3)):
    for j in range(len(img3[i])):
        if [img3[i][j][:3]] == [255, 0, 255]:
            img3[i][j] = (0, 0, 0)
            print(img3[i][j])

stack = bot.stack_images([img, img2, img3], 2)

cv2.imshow('imgs', stack)

cv2.waitKey(0)