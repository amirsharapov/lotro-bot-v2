import datetime
import os
from skimage.util import compare_images

import PIL.Image
import cv2
import numpy as np

from bots.image_processing_bot.ImageProcessingBotService import ImageProcessingBotService
from utils import constants

bot = ImageProcessingBotService()

images = []

for i in os.listdir(constants.TRAINING_DATA_PATH):
    c = cv2.imread(f'{constants.TRAINING_DATA_PATH}\\{i}')
    c = np.array(c)
    images.append(c)

im1 = images[0]
res = None

unique = []
processed = []

for i in images:
    if len(unique) == 0:
        unique.append(i)
        processed.append(i)
    else:
        is_unique = True
        for j in unique:
            # if similar sizes
            if abs(i.shape[0] - j.shape[0]) < 10 and abs(i.shape[1] - j.shape[1]) < 10:
                i = cv2.resize(i, (j.shape[1], j.shape[0]))
                processed.append(i)
                is_unique = False
                break
        if is_unique:
            processed.append(i)
            unique.append(i)

print(len(images))
print(len(processed))

unique2 = []

for i in processed:
    if len(unique2) == 0:
        unique2.append([i])
    else:
        is_unique = True
        for j in unique2:
            if i.shape[:2] == j[0].shape[:2]:
                j.append(i)
                is_unique = False
        if is_unique:
            unique2.append([i])

for i in unique2:
    print(f'{i[0].shape} - {len(i)}')

arr = unique2[1]

im1 = arr[0]
im2 = arr[3]

im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

dif = compare_images(im1, im2, method='blend')

dif = bot.resize_image(dif, 7)
im1 = bot.resize_image(im1, 7)
im2 = bot.resize_image(im2, 7)

cv2.imshow('im1', im1)
cv2.imshow('im2', im2)
cv2.imshow('difference', dif)
cv2.waitKey(0)