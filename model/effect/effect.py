from abc import ABC, abstractmethod


class Effect(ABC):

    @abstractmethod
    def isEnd(self) -> bool:
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass
