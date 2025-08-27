import random

def random_positions(width, height, n):
    positions = set()
    while len(positions) < n:
        positions.add((random.randint(0, width-1), random.randint(0, height-1)))
    return list(positions)