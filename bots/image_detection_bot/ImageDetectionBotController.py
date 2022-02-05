from bots.image_detection_bot.ImageDetectionBotService import ImageDetectionBotService


class ImageDetectionBotController:
    def __init__(self):
        self.service = ImageDetectionBotService()

    def detect_npc_nameplates(self):
        """
        This will run a loop, and identify the NPC nameplates on screen
        :return:
        """
        self.service.detect_yellow_nameplates()
