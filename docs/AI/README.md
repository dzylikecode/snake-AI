# agent

## get state

- 定义蛇的视角为 local, 即 turn left, turn right, straight
- 定义人的视角为 world, 即 up, down, left, right

### danger local

- 复平面视角

  [right, up, left, down] = [1, i, -1, -i]

- 操作

  - straight

    $$next = current * 1$$

  - turn right

    $$next = current / i = current \ast (-i)$$

  - turn left

    $$next = current \ast i $$

  由 $current \rightarrow next$ 可知, 这为一个置换, 也可以看出来是旋转, 联想到同余

  - 考察

    $$[1, i, -1, -i] * i = [i, -1, -i, 1]$$

    用索引替代

    $$[0, 1, 2, 3] \rightarrow [1, 2, 3, 0]$$

    得到 turn left:

    $$next \equiv (current + 1) \pmod 4$$

  - 总结:

    - straight: `next = current`
    - turn left: `next = (current + 1) % 4`
    - turn right: `next = (current - 1) % 4`

- 判断 straight, turn left, turn right 是否有危险

  测试相应位置的危险情况即可

### current world

将当前方位置为 True, 其余为 False

### food sense

食物相对 head 的位置

## get action

- 问题

  tradeoff exploration / exploitation

- 策略

  一开始是随机的, 进行充分地探索, 到后面随着训练的进行, 逐渐倾向于模型的预测

  ```python
  epsilon = 100 - trains_num
  if random.randint(0, 200) < epsilon: # 小于一半的概率随机生成
      random_action()
  else:
      model.predict()
  ```

- 翻译

  将人工智能的数据格式转化为游戏的数据格式, 给游戏执行

## get feedback

- 搜集反馈

  [new_state, reward, score, game_over]

  - game_over

    game_over 不是用来反馈的, 而是游戏如果结束了, 则模型应该不能预测下一步, 后续的预测的任何结果应该都是非法的

- 记录数据

  采用双端队列, 随着训练的进行, 该开始的记忆应该要被遗忘

## 补充

有可能策略陷入死循环, 这时候需要监视. 可以考虑算法的有效性, 超过一定次数, 直接惩罚这次训练,并且结束

```python
if msg == 'msg_game_reset':
    self.loop_num = 0
elif msg == 'msg_loop_end':
    self.loop_num += 1
    if self.loop_num > 100 * len(params['snake']):
        self.AI_hook('msg_train_too_long', params)  # 发送消息
        params['game_over'] = True
```
