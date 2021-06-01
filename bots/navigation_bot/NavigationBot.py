import time

from bots.image_processing_bot.ImageProcessingBotService import ImageProcessingBotService
from utils import constants, game_constants


class NavigationBot:

    def __init__(self):
        self.image_processing_bot = ImageProcessingBotService()
        self.mini_map_rect = game_constants.LOCATIONS['mini_map']

    def get_mini_map(self):
        img = self.image_processing_bot.screenshot()
        return self.image_processing_bot.get_img_segment(img, self.mini_map_rect)

