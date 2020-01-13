import copy
import random

import numpy as np
from environments.AbstractEnvironment import AbstractEnvironment

class OneDayEnvironment(AbstractEnvironment):

    def __init__(self, history, market_cap=0, money=100, delta = 0.01):

        super(OneDayEnvironment, self).__init__()
        self.num_step = 0
        self.market_cap = market_cap
        self.money = money
        self.history = copy.copy(history)
        self.last_state = None
        self.delta = delta

        self.last_date = None


    def step(self, action):

        current_state = self.history[self.num_step]
        now_date, now_open, now_close, now_high, now_low, now_volume = current_state
        if self.last_state == None:
            self.last_state = current_state
        if self.last_date == None:
            self.last_date = now_date

        now_date, last_open, last_close, last_high, last_low, last_volume = self.last_state
        difa = now_close - last_close
        if np.abs(difa) < self.delta:
            difa = 0
        disc = np.sign(difa)

        if action == disc:
            reward = 1
        else:
            reward = -1

        self.money = self.money + action * now_close

        self.num_step+=1
        self.done = False
        if self.num_step >= len(self.history) or self.last_date != now_date:
            self.done = True

        now_date, next_open, next_close, next_high, next_low, next_volume = self.history[self.num_step]

        next_state = np.array([next_open, next_close, next_high, next_low])

        info = {'money':self.money}
        return reward, next_state, self.done, info

    def sample(self):

        return random.choice(self.action_space)