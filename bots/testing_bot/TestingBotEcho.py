from bots.image_detection_bot.ImageDetectionBotService import ImageDetectionBotService
from bots.image_processing_bot.ImageProcessingBotService import ImageProcessingBotService

detection_bot = ImageDetectionBotService()
processing_bot = ImageProcessingBotService()

img = processing_bot.screenshot()

detection_bot.detect_yellow_nameplates(img)