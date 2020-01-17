import copy
import random

import numpy as np

from agents.statics import action_SELL, action_HOLD, action_BUY
from environments.AbstractEnvironment import AbstractEnvironment


class DayByDayEnvironment(AbstractEnvironment):

    def __init__(self, history, market_cap=0, money=100, stock=0, delta = 0.01, inflation = 0.001, num_ops = 77, comision=0.001):

        super(DayByDayEnvironment, self).__init__()
        self.num_step = 0
        self.market_cap = market_cap
        self.money = money
        self.stock = stock
        self.initial_money = money
        self.history = copy.copy(history)
        self.last_state = None
        self.delta = delta
        self.inflation = inflation
        self.num_ops = num_ops
        self.comision = comision

        self.pointer = 0
        self.offset = self.compute_offset()

        self.action_space = np.array([action_SELL, action_HOLD, action_BUY])
        self.current_state = self.make_state_from_history(self.get_index())

        self.last_date = None

    def reset(self):
        self.last_date = None
        self.num_step = 0
        self.offset = self.compute_offset()
        self.money = self.initial_money
        self.current_state = self.make_state_from_history(self.get_index())
        return self.current_state

    def step(self, action):

        current_state = self.history[self.get_index()]
        now_date, now_open, now_close, now_high, now_low, now_volume = current_state
        if self.last_state == None:
            self.last_state = current_state
        if self.last_date == None:
            self.last_date = now_date

        prev_money = self.money + self.stock * now_close
        now_date, last_open, last_close, last_high, last_low, last_volume = self.last_state

        fig = int(self.money / now_close) * now_close
        if action == action_BUY:
            self.stock += int(self.money / now_close)
            self.money -= fig + self.compute_comision(fig)
        elif action == action_SELL:
            self.money += fig + self.compute_comision(fig)
            self.stock -= int(self.money / now_close)

        self.num_step+=1
        self.done = False
        if self.num_step >= self.num_ops or self.money <= now_open and self.stock <= 0: # or self.last_date != now_date:
            self.done = True
            self.money *= 1 - self.inflation
            self.pointer += self.num_ops

        idx = self.get_index()
        now_date, next_open, next_close, next_high, next_low, next_volume = self.history[idx]

        now_money = self.money + self.stock * next_close

        reward = np.sign(now_money - prev_money)
        reward = now_money - prev_money
        if np.abs(reward) <= self.compute_comision(fig) and action == action_HOLD:
                reward = 0
        else:
                reward = -self.inflation

        next_state = np.array([next_open, next_close, next_high, next_low, next_volume])

        info = {'money':self.money, 'stock':self.stock, 'next': next_close}
        return reward, next_state, self.done, info

    def get_action_space(self):
        return len(self.action_space)

    def get_state_space(self):
        return len(self.make_state_from_history(self.get_index()))

    def make_state_from_history(self, i):

        state = []
        for s in self.history[i][1:]:
            state.append(float(s))
        return np.array(state)

    def sample(self):
        return random.choice(self.action_space)

    def compute_offset(self):

        #i = random.randint(0, len(self.history) - self.num_ops)
        i = self.pointer
        xl = (len(self.history) - self.num_ops) - 1
        if i > xl:
            i = xl

        return(i)

    def get_index(self):

        return self.offset + self.num_step - 1

    def compute_comision(self, fig):

        c = self.comision * fig

        c = 0.001
        return (c)