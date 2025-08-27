import numpy as np

class GameMap:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)  # 0=empty, 1=house, 2=zombie, 3=agent

    def add_house(self, pos):
        self.grid[pos[1], pos[0]] = 1

    def add_zombie(self, pos):
        self.grid[pos[1], pos[0]] = 2

    def add_agent(self, pos):
        self.grid[pos[1], pos[0]] = 3

    def clear_cell(self, pos):
        self.grid[pos[1], pos[0]] = 0

    def get_cell(self, pos):
        return self.grid[pos[1], pos[0]]

    def show(self, agents, zombies, houses, camera_pos=(0,0), camera_size=10):
        x0, y0 = camera_pos
        x1, y1 = min(self.width, x0+camera_size), min(self.height, y0+camera_size)
        subgrid = self.grid[y0:y1, x0:x1].copy()
        for agent in agents:
            ax, ay = agent.x, agent.y
            if x0 <= ax < x1 and y0 <= ay < y1:
                subgrid[ay-y0, ax-x0] = 9  # رمز اللاعب
        for zombie in zombies:
            zx, zy = zombie.x, zombie.y
            if x0 <= zx < x1 and y0 <= zy < y1:
                subgrid[zy-y0, zx-x0] = 8  # رمز الزومبي
        for hx, hy in houses:
            if x0 <= hx < x1 and y0 <= hy < y1:
                subgrid[hy-y0, hx-x0] = 7  # رمز البيت
        return subgrid