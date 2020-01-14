from abc import ABCMeta, abstractmethod
import numpy as np
class AbstractEnvironment(metaclass=ABCMeta):

    def __init__(self, *args, **kwargs):
        self.queries = 0

        self.action_space = None
        self.done = False

        self.current_state = None
        self.history = []

    @abstractmethod
    def get_action_space(self):
        pass

    @abstractmethod
    def get_state_space(self):
        pass

    def reset(self):
        self.queries = 0

    @abstractmethod
    def step(self, action):
        pass
