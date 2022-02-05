import cv2

from bots.image_processing_bot.ImageProcessingBotService import ImageProcessingBotService
from utils import game_constants


class NavigationBotService:

    def __init__(self):
        self.image_processing_bot = ImageProcessingBotService()
        self.mini_map_rect = game_constants.LOCATIONS['mini_map']
        self.mini_map_cropped_rect = game_constants.LOCATIONS['mini_map_cropped']

    def get_mini_map(self):
        img = self.image_processing_bot.screenshot()
        return self.image_processing_bot.get_img_segment(img, self.mini_map_rect)

    def get_mini_map_cropped(self):
        img = self.get_mini_map()
        return self.image_processing_bot.get_img_segment(img, self.mini_map_cropped_rect)
