from map import GameMap
from agent import Agent
from zombie import Zombie
from utils import random_positions
from data.save_load import save_game, load_game
from rich import print
from ui.gui import run_gui
import time
import os
import numpy as np

WIDTH, HEIGHT = 20, 20
NUM_AGENTS = 4
NUM_ZOMBIES = 3
NUM_HOUSES = 5
CAMERA_SIZE = 10
SAVE_FILE = "data/saves/game_state.json"

def agents_from_data(agent_data):
    return [Agent(d["id"], d["x"], d["y"]) for d in agent_data]

def zombies_from_data(zombie_data):
    return [Zombie(d["id"], d["x"], d["y"], d["strength"]) for d in zombie_data]

def main():
    if os.path.exists(SAVE_FILE):
        data = load_game(SAVE_FILE)
        game_map = GameMap(WIDTH, HEIGHT)
        game_map.grid = np.array(data["map"])
        agents = agents_from_data(data["agents"])
        zombies = zombies_from_data(data["zombies"])
        house_positions = data["houses"]
        print("[bold green]تم استرجاع حالة اللعبة[/bold green]")
    else:
        game_map = GameMap(WIDTH, HEIGHT)
        house_positions = random_positions(WIDTH, HEIGHT, NUM_HOUSES)
        agent_positions = random_positions(WIDTH, HEIGHT, NUM_AGENTS)
        zombie_positions = random_positions(WIDTH, HEIGHT, NUM_ZOMBIES)

        agents = [Agent(i+1, x, y) for i, (x, y) in enumerate(agent_positions)]
        zombies = [Zombie(i+1, x, y) for i, (x, y) in enumerate(zombie_positions)]

        for hx, hy in house_positions:
            game_map.add_house((hx, hy))

    turns = 0
    while turns < 100:
        for zombie in zombies:
            zombie.move(WIDTH, HEIGHT)
        for agent in agents:
            action = agent.decide(game_map, zombies, house_positions)
            if action == "move":
                agent.move(WIDTH, HEIGHT)
            elif action == "heal":
                agent.heal()
            elif action == "run":
                agent.move(WIDTH, HEIGHT)
            elif action == "attack":
                for zombie in zombies:
                    dist = abs(zombie.x - agent.x) + abs(zombie.y - agent.y)
                    if dist <= 1:
                        zombie.strength -= 10
                        if zombie.strength <= 0:
                            zombies.remove(zombie)
                        break
            elif action == "wait":
                pass
            for zombie in zombies:
                if abs(zombie.x - agent.x) + abs(zombie.y - agent.y) == 0:
                    agent.attacked(zombie.strength, WIDTH, HEIGHT)
        camera_pos = (max(0, agents[0].x - CAMERA_SIZE//2), max(0, agents[0].y - CAMERA_SIZE//2))
        subgrid = game_map.show(agents, zombies, house_positions, camera_pos, CAMERA_SIZE)
        print(f"[bold yellow]Turn {turns+1}[/bold yellow], Agents health: {[agent.health for agent in agents]}")
        print(subgrid)
        time.sleep(0.1)
        turns += 1

        # حفظ الحالة كل 20 دورة
        if turns % 20 == 0:
            save_game(SAVE_FILE, agents, zombies, house_positions, game_map)
            print("[bold green]تم حفظ حالة اللعبة[/bold green]")

    save_game(SAVE_FILE, agents, zombies, house_positions, game_map)
    print("[bold green]تم حفظ حالة اللعبة النهائية في نهاية الحلقة[/bold green]")

    # عرض واجهة رسومية
    run_gui(game_map, agents, zombies, house_positions, camera_pos, CAMERA_SIZE, turns=100)

if __name__ == "__main__":
    main()