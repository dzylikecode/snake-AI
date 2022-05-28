from ..snake.snake_game import Direction
import numpy as np


def Agent2Game_action(agent_action):
    # [straight, right, left]
    clock_wise = [
        Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP
    ]
    idx = clock_wise.index(self.direction)

    if np.array_equal(action, [1, 0, 0]):
        new_dir = clock_wise[idx]  # no change
    elif np.array_equal(action, [0, 1, 0]):
        next_idx = (idx + 1) % 4
        new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
    else:  # [0, 0, 1]
        next_idx = (idx - 1) % 4
        new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

    return new_dir