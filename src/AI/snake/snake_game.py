import pygame
from enum import Enum
from collections import namedtuple
import random


###############################################################################
# type
class Direction(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3


# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

Point = namedtuple('Point', 'x, y')

###############################################################################
# data
snake_state = {
    'head': None,
    'snake': [],
    'score': 0,
    'food': None,
    'game_over': False,
    'input': None,
    'action': None,
    'msg_loop_start': None,
    'msg_loop_end': None,
    'msg_game_reset': None,
    'msg_game_over': None,
    'msg_game_input': 'input',
    'msg_game_action': 'action',
    'msg_game_execute': None,
    'msg_game_ui_before': None,
    'msg_game_ui_after': None,
    'msg_snake_hit_boundary': None,
    'msg_snake_hit_self': None,
    'msg_snake_eat_food': None,
}

###############################################################################
# settins
BLOCK_SIZE = 20
SPEED = 20


def Hook(message, params):
    pass


class SnakeGame:
    def __init__(self, hook=Hook, w=640, h=480, right_paddle=0):
        self.hook = hook
        self.state = snake_state
        self._init_game_platform(w, h, right_paddle)
        self.reset()

    def _init_game_platform(self, w, h, right_paddle):
        self.w = w
        self.h = h
        # init display
        pygame.init()
        self.display = pygame.display.set_mode((self.w + right_paddle, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(r'src/AI/snake/RES/arial.ttf', 25)

    def reset(self):
        self.state['game_over'] = False
        self.state['action'] = Direction.RIGHT
        self.state['head'] = Point(self.w / 2, self.h / 2)
        self.state['snake'] = [
            self.state['head'],
            Point(self.state['head'].x - BLOCK_SIZE, self.state['head'].y),
            Point(self.state['head'].x - BLOCK_SIZE * 2, self.state['head'].y),
        ]
        self.state['score'] = 0
        self._place_food()
        self.hook('msg_game_reset', self.state)

    def start(self):
        while True:
            self.hook('msg_loop_start', self.state)
            if self.state['game_over']:
                self.hook('msg_game_over', self.state)
                self.end()
                break
            self.state['input'] = pygame.event.get()
            self.hook('msg_game_input', self.state)
            self.state['action'] = self._translate_event(self.state['input'])
            self.hook('msg_game_action', self.state)
            self._exe_action(self.state['action'])
            self.hook('msg_game_execute', self.state)
            self._draw_ui()
            self.hook('msg_loop_end', self.state)
            self.clock.tick(SPEED)  # 控制帧率

    def end(self):
        pass

    def __del__(self):
        pygame.quit()
        quit()

    def _translate_event(self, events):
        direct = self.state['action']
        for event in events:
            if event.type == pygame.QUIT:
                self.state['game_over'] = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direct = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    direct = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    direct = Direction.UP
                elif event.key == pygame.K_DOWN:
                    direct = Direction.DOWN
        return direct

    def _exe_action(self, action):
        self._move(action)
        self.state['snake'].insert(0, self.state['head'])
        if self.state['head'] == self.state['food']:
            self.hook('msg_snake_eat_food', self.state)
            self.state['score'] += 1
            self._place_food()
        else:
            self.state['snake'].pop()
        if self._is_collision():
            self.state['game_over'] = True

    def _move(self, action):
        x = self.state['head'].x
        y = self.state['head'].y
        if action == Direction.RIGHT:
            x += BLOCK_SIZE
        elif action == Direction.LEFT:
            x -= BLOCK_SIZE
        elif action == Direction.UP:
            y -= BLOCK_SIZE
        elif action == Direction.DOWN:
            y += BLOCK_SIZE
        self.state['head'] = Point(x, y)

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.state['food'] = Point(x, y)
        if self.state['food'] in self.state['snake']:
            self._place_food()  # 递归到不重合为止

    def _is_collision(self):
        # hits boundary
        pt = self.state['head']
        if (pt.x > self.w - BLOCK_SIZE or pt.x < 0
                or pt.y > self.h - BLOCK_SIZE or pt.y < 0):
            self.hook('msg_snake_hit_boundary', self.state)
            return True
        # hits itself
        if pt in self.state['snake'][1:]:
            self.hook('msg_snake_hit_self', self.state)
            return True
        return False

    def is_collision(self, pt):
        # hits boundary
        if (pt.x > self.w - BLOCK_SIZE or pt.x < 0
                or pt.y > self.h - BLOCK_SIZE or pt.y < 0):
            return True
        # hits itself
        if pt in self.state['snake'][1:]:
            return True
        return False

    def _draw_ui(self):
        self.display.fill(BLACK)
        self.hook('msg_game_ui_before', self.state)
        for pt in self.state['snake']:
            pygame.draw.rect(self.display, BLUE1,
                             pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(
                self.display, BLUE2,
                pygame.Rect(pt.x + 4, pt.y + 4, BLOCK_SIZE - 2 * 4,
                            BLOCK_SIZE - 2 * 4))

        pygame.draw.rect(
            self.display, RED,
            pygame.Rect(self.state['food'].x, self.state['food'].y, BLOCK_SIZE,
                        BLOCK_SIZE))

        text = self.font.render("Score: " + str(self.state['score']), True,
                                WHITE)
        self.display.blit(text, [0, 0])
        self.hook('msg_game_ui_after', self.state)
        pygame.display.flip()


if __name__ == '__main__':
    game = SnakeGame()
    game.start()
