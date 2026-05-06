from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    def __init__(self, params):
        self.params = params

    @abstractmethod
    def generate_signal(self, df):
        pass