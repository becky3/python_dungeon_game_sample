import pygame

from const import Color
from model.draw_object.draw_object import DrawObject


class Rect(DrawObject):

    def __init__(self,
                 position: (int, int),
                 size: (int, int),
                 fill_color: int = Color.BLACK,
                 is_absolute_position=False
                 ):
        super().__init__(position, is_absolute_position)
        self.__size = size
        self.__fill_color = fill_color

    def draw(self, display: pygame.display, adjust: (int, int)):
        x = self.x - adjust[0]
        y = self.y - adjust[1]
        width, height = self.__size
        pygame.draw.rect(
            display,
            self.__fill_color,
            [x, y, width, height]
        )
