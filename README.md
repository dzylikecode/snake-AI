# snake-AI

- repository:[snake AI](https://github.com/python-engineer/snake-ai-pytorch)
- video: [Teach AI To Play Snake - Reinforcement Learning Tutorial With PyTorch And Pygame](https://www.youtube.com/watch?v=PJl4iabBEz0&list=PLqnslRFeH2UrDh7vUmJ60YrmWd64mTTKV)
- series: [Teach AI To Play Snake - Reinforcement Learning Tutorial With PyTorch And Pygame (Part 1)](https://www.youtube.com/watch?v=PJl4iabBEz0&list=RDCMUCbXgNpp0jedKWcQiULLbDTA&start_radio=1)

## preview struct

- :boat:

  当前文件夹的封面或者根目录

- exercise

  习题

- book

  学习的主要知识

## command usage

- 激活常用命令

  ```bash
  source ./command.sh
  ```

- 创建环境

  make

  ```bash
  dz_mk
  ```

- 删除环境

  remove

  ```bash
  dz_rm
  ```

- 进入环境

  ```bash
  dz_cd
  ```

- 离开环境

  left

  ```bash
  dz_lf
  ```

- 导入环境

  import

  ```bash
  dz_im
  ```

- 导出环境

  ```bash
  dz_ex
  ```

### example

install pytorch

```bash
dz_in pytorch torchvision torchaudio pytorch-cuda=11.6 -c pytorch -c nvidia
```

## install

1. prepare for virtual environment

   ```bash
   dz_mk
   ```

2. install pygame

   ```bash
   dz_cd
   ```

   - [how to install pygame](https://www.pygame.org/wiki/GettingStarted)

   - linux ubuntu

     ```bash
     sudo apt-get install python3-pygame
     ```

     recommend:

     ```bash
     python3 -m pip install -U pygame --user
     ```

3. play

   - play snake

     ```bash
     dz_snake
     ```

   - play snake with AI

     ```bash
     dz_ai
     ```

## issue

- [Could not load the Qt platform plugin "xcb" in "" even though it was found](https://askubuntu.com/questions/1271976/could-not-load-the-qt-platform-plugin-xcb-in-even-though-it-was-found)
- [Could not find or load the Qt platform plugin "xcb"](https://stackoverflow.com/questions/33051790/could-not-find-or-load-the-qt-platform-plugin-xcb)

  solved:

  ```py
  import matplotlib
  matplotlib.use('TkAgg')
  ```
