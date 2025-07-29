import gymnasium as gym
import ale_py

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

gym.register_envs(ale_py)

env = gym.make('ALE/Pong-v5', obs_type='rgb', render_mode='human')

env.reset()
while True:
    env.step(0)
    env.render()