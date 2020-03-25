import copy
import random

import numpy as np

from agents.statics import action_HOLD, action_BUY, action_SELL
from environments.AbstractEnvironment import AbstractEnvironment

class FullHistoryEnvironment(AbstractEnvironment):

    def __init__(self, history, market_cap=0, money=100, delta = 0.01, inflation = 0.0):

        super(FullHistoryEnvironment, self).__init__()
        self.num_step = 0
        self.market_cap = market_cap
        self.money = money
        self.stock = 0
        self.initial_money = money
        self.history = copy.copy(history)
        self.last_state = None
        self.delta = delta
        self.inflation = inflation

        from agents.statics import action_SELL
        self.action_space = np.array([action_SELL, action_HOLD, action_BUY])
        self.current_state = self.make_state_from_history(self.num_step)

        self.last_date = None

    def reset(self):
        self.last_date = None
        self.num_step = 0
        self.money = self.initial_money
        self.current_state = self.make_state_from_history(self.num_step)
        return self.current_state

    def step(self, action):

        current_state = self.history[self.num_step]
        now_date, now_open, now_close, now_high, now_low, now_volume = current_state
        if self.last_state == None:
            self.last_state = current_state
        if self.last_date == None:
            self.last_date = now_date

        prev_money = self.money + self.stock * now_close
        now_date, last_open, last_close, last_high, last_low, last_volume = self.last_state

        if action == action_BUY:
            self.money -= now_close
            self.stock += 1
        elif action == action_SELL:
            self.money += now_close
            self.stock -= 1

        self.num_step+=1
        self.done = False
        if self.num_step >= len(self.history)-1 or self.money <= now_open and self.stock <= 0: # or self.last_date != now_date:
            self.done = True
            self.money *= (1 - self.inflation)

        now_date, next_open, next_close, next_high, next_low, next_volume = self.history[self.num_step]

        now_money = self.money + self.stock * next_close

        reward = np.sign(now_money - prev_money)
        if reward == 0 and action == action_HOLD:
            reward = 1
        elif reward==0 and action != action_HOLD:
            reward = -1
        next_state = np.array([next_open, next_close, next_high, next_low, next_volume])

        info = {'money':self.money, 'stock':self.stock, 'next': next_close}
        return reward, next_state, self.done, info

    def get_action_space(self):
        return len(self.action_space)

    def get_state_space(self):
        return len(self.make_state_from_history(self.num_step))

    def make_state_from_history(self, i):

        state = []
        for s in self.history[i][1:]:
            state.append(float(s))
        return np.array(state)

    def sample(self):
        return random.choice(self.action_space)