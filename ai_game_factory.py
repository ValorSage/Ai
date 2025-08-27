import random

BOARD_SIZE = 10
NUM_PLAYERS = 4
NUM_ZOMBIES_START = 2
NUM_ATTEMPTS = 100
MEM_TRAIN_INTERVAL = 20

class Agent:
    def __init__(self, idx):
        self.idx = idx
        self.health = 100
        self.memory = []
        self.x = random.randint(0, BOARD_SIZE-1)
        self.y = random.randint(0, BOARD_SIZE-1)

    def decide_action(self, board, zombies, houses):
        # يستخدم الذاكرة لتغيير الاستراتيجية
        if self.health < 30 and (self.x, self.y) in houses:
            return "heal"
        # إذا زومبي قريب اهرب أو هاجم
        for zx, zy in zombies:
            if abs(zx - self.x) + abs(zy - self.y) <= 1:
                return random.choice(["attack", "run"])
        # غير ذلك يتحرك عشوائي
        return random.choice(["move", "wait"])

    def train(self):
        # يحلل الذاكرة ويحسن الاستراتيجية (بسيط هنا، لكن ممكن تطويره)
        if len(self.memory) >= MEM_TRAIN_INTERVAL:
            # مثال: إذا مات كثيرًا، يحاول الهروب أكثر
            deaths = sum(1 for mem in self.memory[-MEM_TRAIN_INTERVAL:] if mem["result"] == "dead")
            if deaths > 8:
                print(f"Agent {self.idx} will try to escape more!")
            self.memory = [] # يمسح الذاكرة بعد التدريب

class Zombie:
    def __init__(self, strength):
        self.strength = strength
        self.x = random.randint(0, BOARD_SIZE-1)
        self.y = random.randint(0, BOARD_SIZE-1)

def init_houses(num=3):
    # أماكن علاج عشوائية
    return [(random.randint(0, BOARD_SIZE-1), random.randint(0, BOARD_SIZE-1)) for _ in range(num)]

def move_entity(x, y):
    # حركة عشوائية
    dx, dy = random.choice([(0,1), (1,0), (0,-1), (-1,0), (0,0)])
    nx, ny = max(0, min(BOARD_SIZE-1, x+dx)), max(0, min(BOARD_SIZE-1, y+dy))
    return nx, ny

def main():
    agents = [Agent(i) for i in range(NUM_PLAYERS)]
    houses = init_houses()
    zombies = [Zombie(strength=10) for _ in range(NUM_ZOMBIES_START)]

    for attempt in range(NUM_ATTEMPTS):
        print(f"--- Attempt {attempt+1} ---")
        # حركة الزومبي وتطورهم
        for z in zombies:
            z.x, z.y = move_entity(z.x, z.y)
        if attempt % 10 == 0:  # كل 10 جولات يزداد عدد الزومبي ويقوى
            zombies.append(Zombie(strength=10 + attempt//10*5))

        # حركة وتفاعل اللاعبين
        for agent in agents:
            action = agent.decide_action(None, [(z.x, z.y) for z in zombies], houses)
            if action == "move":
                agent.x, agent.y = move_entity(agent.x, agent.y)
            elif action == "attack":
                # إذا زومبي قريب يهاجمه
                for z in zombies:
                    if abs(z.x - agent.x) + abs(z.y - agent.y) <= 1:
                        z.strength -= 10
                        agent.memory.append({"action": "attack", "result": "success"})
                        if z.strength <= 0:
                            zombies.remove(z)
                        break
            elif action == "run":
                agent.x, agent.y = move_entity(agent.x, agent.y)
                agent.memory.append({"action": "run", "result": "success"})
            elif action == "heal":
                agent.health = min(100, agent.health + 50)
                agent.memory.append({"action": "heal", "result": "success"})
            elif action == "wait":
                agent.memory.append({"action": "wait", "result": "success"})

            # تحقق من هجوم الزومبي
            for z in zombies:
                if abs(z.x - agent.x) + abs(z.y - agent.y) == 0:
                    agent.health -= z.strength
                    if agent.health <= 0:
                        agent.memory.append({"action": "dead", "result": "dead"})
                        agent.health = 100  # يعاد إحياءه في مكان عشوائي
                        agent.x, agent.y = random.randint(0, BOARD_SIZE-1), random.randint(0, BOARD_SIZE-1)
            # تدريب كل فترة
            if attempt % MEM_TRAIN_INTERVAL == 0 and attempt != 0:
                agent.train()

        # طباعة حالة كل لاعب
        for agent in agents:
            print(f"Agent {agent.idx}: Health={agent.health}, Position=({agent.x},{agent.y})")

if __name__ == "__main__":
    main()