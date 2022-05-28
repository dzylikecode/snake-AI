from collections import deque
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

MAX_MEMORY = 100_000


class DateSet:
    """如果记忆库已满，则淘汰最旧的一条记录"""
    def __init__(self, size=MAX_MEMORY):
        self.size = size
        self.data = deque(maxlen=size)
        self.cur_data = None

    def record(self, state, action, feedback):
        self.data.append((state, action, feedback['reward'], feedback['state'],
                          feedback['game_over']))
        self.cur_data = (state, action, feedback['reward'], feedback['state'],
                         feedback['game_over'])


class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)  # 输入层 -> 中间层
        self.linear2 = nn.Linear(hidden_size, output_size)  # 中间层 -> 输出层

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class DQL:
    def __init__(self, input_size, hidden_size, output_size):
        self.model = Linear_QNet(input_size, hidden_size, output_size)
        self.learning_rate = 0.001
        self.gamma = 0.9
        self.optimizer = optim.Adam(self.model.parameters(),
                                    lr=self.learning_rate)
        self.criterion = nn.MSELoss()  # 损失函数形式

    def predict(self, state):
        state = torch.tensor(state, dtype=torch.float)
        prediction = self.model(state)
        action = [False, False, False]
        index = torch.argmax(prediction).item()  # 取出最大值的索引
        action[index] = True
        return action

    def train(self, state, action, reward, next_state, game_over):
        # predicted Q values with current state
        pred_action = self.model(state)
        # Q_new = r + y * max(next_predicted Q value)
        target = pred_action.clone()
        for i in range(len(game_over)):
            Q_new = reward[i]
            if not game_over[i]:  # 注意游戏结束是不存在下一步
                Q_new = reward[i] + self.gamma * torch.max(
                    self.model(next_state[i]))

            target[i][torch.argmax(action[i]).item()] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target, pred_action)
        loss.backward()

        self.optimizer.step()

    def train_short(self, state, action, reward, next_state, game_over):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        state = torch.unsqueeze(state, 0)
        next_state = torch.unsqueeze(next_state, 0)
        action = torch.unsqueeze(action, 0)
        reward = torch.unsqueeze(reward, 0)
        game_over = (game_over, )
        self.train(state, action, reward, next_state, game_over)

    def train_whole(self, state, action, reward, next_state, game_over):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        self.train(state, action, reward, next_state, game_over)
