import random

class Zombie:
    def __init__(self, idx, x, y, strength=15):
        self.idx = idx
        self.x = x
        self.y = y
        self.strength = strength
        self.icon = f"Z{idx}"

    def move(self, width, height):
        dx, dy = random.choice([(0,1),(1,0),(0,-1),(-1,0),(0,0)])
        self.x = max(0, min(width-1, self.x+dx))
        self.y = max(0, min(height-1, self.y+dy))