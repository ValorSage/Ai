import pygame
import sys

CELL_SIZE = 32
AGENT_COLOR = (0, 120, 255)
ZOMBIE_COLOR = (180, 0, 0)
HOUSE_COLOR = (40, 220, 40)
EMPTY_COLOR = (230, 230, 230)
BG_COLOR = (200, 200, 200)

def draw_grid(screen, grid, agents, zombies, houses, camera_pos, camera_size):
    x0, y0 = camera_pos
    for i in range(camera_size):
        for j in range(camera_size):
            pos_x = x0 + j
            pos_y = y0 + i
            rect = pygame.Rect(j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            cell_val = 0
            if 0 <= pos_x < grid.shape[1] and 0 <= pos_y < grid.shape[0]:
                cell_val = grid[pos_y, pos_x]
            color = EMPTY_COLOR
            if cell_val == 1:
                color = HOUSE_COLOR
            screen.fill(BG_COLOR, rect)
            pygame.draw.rect(screen, color, rect, 0)
            pygame.draw.rect(screen, (100,100,100), rect, 1)
    for agent in agents:
        ax, ay = agent.x - x0, agent.y - y0
        if 0 <= ax < camera_size and 0 <= ay < camera_size:
            rect = pygame.Rect(ax*CELL_SIZE, ay*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.circle(screen, AGENT_COLOR, rect.center, CELL_SIZE//2-4)
    for zombie in zombies:
        zx, zy = zombie.x - x0, zombie.y - y0
        if 0 <= zx < camera_size and 0 <= zy < camera_size:
            rect = pygame.Rect(zx*CELL_SIZE, zy*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.circle(screen, ZOMBIE_COLOR, rect.center, CELL_SIZE//2-6)
    for hx, hy in houses:
        hxg, hyg = hx-x0, hy-y0
        if 0 <= hxg < camera_size and 0 <= hyg < camera_size:
            rect = pygame.Rect(hxg*CELL_SIZE, hyg*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, HOUSE_COLOR, rect, 0)

def run_gui(game_map, agents, zombies, houses, camera_pos, camera_size, turns=100):
    pygame.init()
    screen = pygame.display.set_mode((CELL_SIZE*camera_size, CELL_SIZE*camera_size))
    pygame.display.set_caption("AI Game Factory GUI")
    clock = pygame.time.Clock()
    running = True
    turn = 0
    while running and turn < turns:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_grid(screen, game_map.grid, agents, zombies, houses, camera_pos, camera_size)
        pygame.display.flip()
        clock.tick(4)
        turn += 1
    pygame.quit()
    sys.exit()