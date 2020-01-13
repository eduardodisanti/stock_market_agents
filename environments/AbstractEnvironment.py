from abc import ABCMeta, abstractmethod
import numpy as np

action_SELL = 1
action_HOLD = 0
action_BUY  = -1

class AbstractEnvironment(metaclass=ABCMeta):

    def __init__(self, *args, **kwargs):
        self.queries = 0

        self.action_space = np.array([action_SELL, action_HOLD, action_BUY])
        self.done = False

        _OPEN = _CLOSE = _HIGH = _LOW = _VOLUME = _MONEY = 0
        self.current_state = np.array([_OPEN, _CLOSE, _HIGH, _LOW, _VOLUME, _MONEY])
        self.history = []

    def get_action_space(self):
        return self.action_space

    def get_state_space(self):
        return self.current_state

    def reset(self):
        self.queries = 0

    @abstractmethod
    def step(self, action):
        pass
