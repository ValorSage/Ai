import random

class AIModel:
    def get_action(self, player, memory):
        # تحليل الذاكرة واختيار أفضل فعل
        if player.health < 30:
            return "go_to_shelter"
        elif random.random() < 0.5:
            return "attack_zombie"
        else:
            return "run_away"

    def train(self, memory):
        # بعد 20 محاولة، يراجع الذاكرة ويعدل استراتيجيته
        pass