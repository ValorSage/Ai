import random
from memory import Memory
from ai.ml_model import AgentMLModel

class Agent:
    def __init__(self, idx, x, y):
        self.idx = idx
        self.x = x
        self.y = y
        self.health = 100
        self.memory = Memory(idx)
        self.icon = f"A{idx}"
        self.strategy = {"escape_bias": 0.5, "heal_bias": 0.5}
        self.ml_model = AgentMLModel(idx)

    def decide(self, world, zombies, houses):
        stats = self.memory.analyze()
        if stats["deaths"] > 10:
            self.strategy["escape_bias"] = 0.8
        if stats["heals"] > 5:
            self.strategy["heal_bias"] = 0.8

        features = [
            1 if self.health < 25 and (self.x, self.y) in houses else 0,
            1 if any(abs(z.x - self.x)+abs(z.y-self.y)<=1 for z in zombies) else 0,
            1 if self.health < 50 else 0,
            random.random()
        ]
        self.ml_model.train()
        ml_decision = self.ml_model.predict(features)
        if ml_decision == 1:
            if self.health < 25 and (self.x, self.y) in houses:
                return "heal"
            for z in zombies:
                dist = abs(z.x - self.x) + abs(z.y - self.y)
                if dist <= 1:
                    return random.choice(["attack", "run"])

        if self.health < 25 and (self.x, self.y) in houses and random.random() < self.strategy["heal_bias"]:
            return "heal"
        for z in zombies:
            dist = abs(z.x - self.x) + abs(z.y - self.y)
            if dist <= 1:
                if random.random() < self.strategy["escape_bias"]:
                    return "run"
                else:
                    return "attack"
        return random.choice(["move", "wait"])

    def move(self, width, height):
        dx, dy = random.choice([(0,1),(1,0),(0,-1),(-1,0),(0,0)])
        self.x = max(0, min(width-1, self.x+dx))
        self.y = max(0, min(height-1, self.y+dy))

    def heal(self):
        self.health = min(100, self.health + 40)

    def attacked(self, damage, width, height):
        self.health -= damage
        if self.health <= 0:
            self.memory.add("dead", "dead")
            self.health = 100
            self.x = random.randint(0, width-1)
            self.y = random.randint(0, height-1)

    def update_memory(self, action, result):
        self.memory.add(action, result)
        self.memory.save()