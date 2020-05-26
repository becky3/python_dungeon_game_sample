import math


class Chip():

    @property
    def dot_size(self) -> (int, int):
        return self.__dot_size

    @property
    def area_size(self) -> (int, int):
        return self.__area_size

    @property
    def item_size(self) -> (int, int):
        return (self.__column, self.__row)

    def __init__(self,
                 dot_size: (int, int),
                 area_size: (int, int),
                 ):
        self.__dot_size = dot_size
        self.__area_size = area_size
        self.__column = area_size[0] / dot_size[0]
        self.__row = area_size[1] / dot_size[1]

    def get_draw_rect(self, index: int) -> (int, int, int, int):
        width, height = self.__dot_size
        x = (index % self.__column) * width
        y = math.floor(index / self.__column) * height

        return (x, y, width, height)
