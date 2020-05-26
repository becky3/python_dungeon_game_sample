import pygame

from model.draw_object.draw_object import DrawObject


class Camera:

    @property
    def size(self) -> (int, int):
        return self.__screen.get_size()

    @property
    def screen(self) -> pygame.Surface:
        return self.__screen

    def __init__(self, size: (int, int), power: int):
        self.__screen = pygame.Surface(size)
        self.x = 0
        self.y = 0
        self.__draw_objects = []
        self.__power = power

    def reset(self):
        self.x = 0
        self.y = 0

    def add_draw_object(self, draw_object: DrawObject):
        self.__draw_objects.append(draw_object)

    def fill(self, color: int):
        self.__screen.fill(color)

    def draw(self):
        for o in self.__draw_objects:
            x, y = self.x, self.y
            if o.is_absolute_position:
                x, y = 0, 0
            o.draw(self.__screen, (x, y))

        self.__draw_objects = []
