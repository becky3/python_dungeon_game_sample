import math

from const import Direction
from model.chip import Chip


class CharacterChip():

    def __init__(self,
                 dot_size: (int, int),
                 area_size: (int, int),
                 max_pattern: int = 2
                 ):
        self.__chip = Chip(dot_size, area_size)
        self.__character_no = 0
        self.__max_pattern = max_pattern

    def set_character_no(self, no: int):
        self.__character_no = no

    def __get_direction_no(self, direction: int) -> int:
        order = Direction.get_order(direction)
        if order == -1:
            order = 2
        return order

    def get_draw_rect(self,
                      direction: int = Direction.DOWN,
                      pattern: int = 0
                      ):

        chip_column = self.__chip.item_size[0]
        max_pattern = self.__max_pattern

        max_oneline_char = chip_column / max_pattern

        character_no = self.__character_no
        char_row = math.floor(character_no / max_oneline_char)
        char_col = character_no % max_oneline_char

        max_direction = 4
        char_detail_row = char_row * max_direction
        char_datail_col = char_col * max_pattern
        direction_no = self.__get_direction_no(direction)
        row = (char_detail_row + direction_no) * chip_column
        col = char_datail_col + (pattern % max_pattern)
        index = row + col

        return self.__chip.get_draw_rect(index)
