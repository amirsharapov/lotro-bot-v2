from bots.detection_bot.DetectionBotService import IdentificationBotService


class IdentificationBot:
    def __init__(self):
        self.service = IdentificationBotService()

    def identify_npc_nameplates(self):
        """
        This will run a loop, and identify the NPC nameplates on screen
        :return:
        """
        self.service.detect_yellow_colors()
