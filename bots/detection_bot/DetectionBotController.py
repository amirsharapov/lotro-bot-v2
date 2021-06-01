from bots.detection_bot.DetectionBotService import DetectionBotService


class IdentificationBot:
    def __init__(self):
        self.service = DetectionBotService()

    def detect_npc_nameplates(self):
        """
        This will run a loop, and identify the NPC nameplates on screen
        :return:
        """
        self.service.detect_yellow_nameplates()
