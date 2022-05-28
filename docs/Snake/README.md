# 贪吃蛇

## translate-event

将游戏的上下左右翻译成蛇的上下左右即可

## execute-action

### snake move

- 蛇:[a1, a2, a3]

- 移动到点 a0, 则插入 a0

  蛇: [a0, a1, a2, a3]

- 如果吃了食物, 则保持

  蛇: [a0, a1, a2, a3]

- 如果没有吃, 则删掉最后一个

  蛇: [a0, a1, a2]

## draw ui

- snake shape

  20x20 的外部, 12x12 的内部, 显得有立体感

