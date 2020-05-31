from abc import ABC, abstractmethod
import math


class Event(ABC):

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def map_coordinate(self) -> (int, int):
        return (math.floor(self.__y), math.floor(self.__x))

    def __init__(self, position: (float, float)):
        self.__y, self.__x = position
        self.width = 16
        self.height = 16

    def set_position(self, position: (float, float)):
        self.__y, self.__x = position

    def add_position(self, value: (float, float)):
        self.__y += value[0]
        self.__x += value[1]

    @abstractmethod
    def draw(self):
        pass
