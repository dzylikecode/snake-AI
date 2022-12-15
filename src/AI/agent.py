from snake.snake_game import SnakeGame, Direction, Point, BLOCK_SIZE
import pygame
import random
from model import DateSet, DQL
from visualize_data import plot

###############################################################################
# settings
BATCH_SIZE = 1000


###############################################################################
# help function
def get_direction_index(direction):
    counter_clock_wise = [
        Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.DOWN
    ]  # 逆时针排列
    return counter_clock_wise.index(direction)


def get_direction_by_index(index):
    counter_clock_wise = [
        Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.DOWN
    ]  # 逆时针排列
    return counter_clock_wise[index]


class SnakeAgent:
    def __init__(self):
        self.game = None
        self.model = DQL(11, 256, 3)
        self.data_set = DateSet()
        self.trains_num = 0
        # 可视化数据
        self.width = 640
        self.height = 480
        self.right_paddle = 150
        self.total_score = 0
        self.score_list = []
        self.mean_score_list = []
        self.max_score = 0

    def get_state(self, game_data):
        head = game_data['head']
        food = game_data['food']
        point_l = Point(head.x - BLOCK_SIZE, head.y)
        point_r = Point(head.x + BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y - BLOCK_SIZE)
        point_d = Point(head.x, head.y + BLOCK_SIZE)
        counter_clock_wise_pos = [point_r, point_u, point_l, point_d]
        # world
        world_msg = [False, False, False, False]
        cur_dir_index = get_direction_index(game_data['action'])
        world_msg[cur_dir_index] = True  # 当前位置为True
        # danger
        # # straight
        nxt_dir_idx = cur_dir_index
        nxt_dir_pos = counter_clock_wise_pos[nxt_dir_idx]
        danger_straight = self.game.is_collision(nxt_dir_pos)
        # # right
        nxt_dir_idx = (cur_dir_index - 1) % 4
        nxt_dir_pos = counter_clock_wise_pos[nxt_dir_idx]
        danger_right = self.game.is_collision(nxt_dir_pos)
        # # left
        nxt_dir_idx = (cur_dir_index + 1) % 4
        nxt_dir_pos = counter_clock_wise_pos[nxt_dir_idx]
        danger_left = self.game.is_collision(nxt_dir_pos)

        danger_msg = [danger_straight, danger_right, danger_left]

        # food
        food_msg = [
            food.x > head.x,  # right
            food.y < head.y,  # up
            food.x < head.x,  # left
            food.y > head.y,  # down
        ]

        state = []
        state.extend(danger_msg)
        state.extend(world_msg)
        state.extend(food_msg)
        return state

    def get_action(self, state):
        epsilon = 100 - self.trains_num
        action = [False, False, False]
        if random.randint(0, 200) < epsilon:
            action[random.randint(0, 2)] = True
        else:
            action = self.model.predict(state)
        return action

    def interpret_action(self, action, params):
        pre_idx = get_direction_index(params['action'])
        if action[0]:  # straight
            return get_direction_by_index(pre_idx)
        elif action[1]:  # right
            return get_direction_by_index((pre_idx - 1) % 4)
        elif action[2]:  # left
            return get_direction_by_index((pre_idx + 1) % 4)

    def get_feedback(self, game_data):
        return {
            'reward': self.reward,
            'state': self.get_state(game_data),
            'game_over': game_data['game_over'],
        }

    def train_whole(self, data_set):
        """回顾整个人生历程"""
        recall_data_set = None
        if len(data_set.data) > BATCH_SIZE:
            recall_data_set = random.sample(data_set.data, BATCH_SIZE)
        else:
            recall_data_set = data_set.data
        state, action, reward, next_state, game_over = zip(*recall_data_set)
        self.model.train_whole(state, action, reward, next_state, game_over)

    def train_short(self, data_set):
        """走一步看一步的策略"""
        state, action, reward, next_state, game_over = data_set.cur_data
        self.model.train_short(state, action, reward, next_state, game_over)

    def play(self):
        self.game = SnakeGame(self.AI_hook, self.width, self.height,
                              self.right_paddle)
        while True:
            self.game.reset()
            self.game.start()
            self.train_whole(self.data_set)

    def AI_hook(self, msg, params):
        # Ai 主题逻辑
        if msg == 'msg_loop_start':
            self.state = self.get_state(params)
        elif msg == 'msg_game_action':
            self.action = self.get_action(self.state)
            params['action'] = self.interpret_action(self.action, params)
        elif msg == 'msg_loop_end':
            self.feedback = self.get_feedback(params)
            self.data_set.record(self.state, self.action, self.feedback)
            self.train_short(self.data_set)
        # 退出AI
        if msg == 'msg_game_input':
            for event in params['input']:
                if event.type == pygame.QUIT:
                    quit()
        # 采集数据
        # # 设置奖励
        # # 训练次数
        if msg == 'msg_loop_start':
            self.reward = 0
        elif msg == 'msg_snake_eat_food':
            self.reward = 10
        elif msg == 'msg_snake_hit_boundary':
            self.reward = -10
        elif msg == 'msg_snake_hit_self':
            self.reward = -10
        elif msg == 'msg_game_over':
            self.trains_num += 1
        elif msg == 'msg_train_too_long':
            self.reward = -10
        # 补充
        if msg == 'msg_game_reset':
            self.loop_num = 0
        elif msg == 'msg_loop_end':
            self.loop_num += 1
            if self.loop_num > 100 * len(params['snake']):
                self.AI_hook('msg_train_too_long', params)  # 发送消息
                params['game_over'] = True
        # 可视化数据
        if msg == 'msg_game_ui_before':
            # action
            font_color = (0, 255, 0)
            if self.action[0]:
                str_action = self.game.font.render('straight', True,
                                                   font_color)
                self.game.display.blit(str_action, (self.width + 2, 0))
            elif self.action[1]:
                str_action = self.game.font.render('turn right', True,
                                                   font_color)
                self.game.display.blit(str_action, (self.width + 2, 0))
            elif self.action[2]:
                str_action = self.game.font.render('turn left', True,
                                                   font_color)
                self.game.display.blit(str_action, (self.width + 2, 0))
            # direction
            str_dir_list = ['right', 'up', 'left', 'down']
            str_dir_idx = get_direction_index(params['action'])
            str_dir = self.game.font.render(str_dir_list[str_dir_idx], True,
                                            font_color)
            self.game.display.blit(str_dir, (self.width + 2, 20))
            # danger
            if self.state[0]:
                str_danger = self.game.font.render('danger straight', True,
                                                   font_color)
                self.game.display.blit(str_danger, (self.width + 2, 40))
            if self.state[1]:
                str_danger = self.game.font.render('danger right', True,
                                                   font_color)
                self.game.display.blit(str_danger, (self.width + 2, 60))
            if self.state[2]:
                str_danger = self.game.font.render('danger left', True,
                                                   font_color)
                self.game.display.blit(str_danger, (self.width + 2, 80))
            # food pos
            if self.state[-4]:
                str_food = self.game.font.render('food right', True,
                                                 font_color)
                self.game.display.blit(str_food, (self.width + 2, 100))
            if self.state[-3]:
                str_food = self.game.font.render('food up', True, font_color)
                self.game.display.blit(str_food, (self.width + 2, 120))
            if self.state[-2]:
                str_food = self.game.font.render('food left', True, font_color)
                self.game.display.blit(str_food, (self.width + 2, 140))
            if self.state[-1]:
                str_food = self.game.font.render('food down', True, font_color)
                self.game.display.blit(str_food, (self.width + 2, 160))
            # reward
            str_reward = self.game.font.render('reward:' + str(self.reward),
                                               True, font_color)
            self.game.display.blit(str_reward, (self.width + 2, 180))
        elif msg == 'msg_game_over':
            self.total_score += params['score']
            self.score_list.append(params['score'])
            self.mean_score_list.append(self.total_score / self.trains_num)
            plot(self.score_list, self.mean_score_list)
            # 储存模型
            if self.max_score < params['score']:
                self.max_score = params['score']
                self.model.save()
            print('Game', self.trains_num, 'Score', self.max_score)


if __name__ == '__main__':
    AI = SnakeAgent()
    AI.play()
