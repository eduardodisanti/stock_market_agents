from abc import ABC, ABCMeta, abstractmethod


class StockDataSource(metaclass=ABCMeta):

    def __init__(self, *args, **kwargs):

        self.queries = 0

    def reset(self):
        self.queries = 0


    @abstractmethod
    def get_live(self):
        pass

    @abstractmethod
    def get_history(self, interval, range):
        pass