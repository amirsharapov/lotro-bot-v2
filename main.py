import os

import cv2

from bots.detection_bot.DetectionBotService import DetectionBotService
from utils import constants

bot = DetectionBotService()

bot.detect_mini_map_facilities()