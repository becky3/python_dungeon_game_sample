from abc import ABC, abstractmethod

import pygame


class DrawObject(ABC):

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def is_absolute_position(self) -> bool:
        return self.__is_absolute_position

    def set_position(self, value: (int, int)):
        self.__x, self.__y = value

    def __init__(self,
                 position: (int, int),
                 is_absolute_position: bool = False
                 ):
        self.__x, self.__y = position
        self.__is_absolute_position = is_absolute_position

    @abstractmethod
    def draw(self, display: pygame.display, adjust: (int, int)):
        pass
