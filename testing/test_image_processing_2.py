import cv2
import numpy as np

from bots.image_processing_bot.ImageProcessingBotService import ImageProcessingBotService
image_processing_bot = ImageProcessingBotService()

img = cv2.imread('img.png')
img = cv2.resize(img, (500, 400))

img2 = image_processing_bot.adjust_contrast(img, 130)

cv2.imshow('image', img)
cv2.imshow('adjusted', img2)

cv2.waitKey(0)