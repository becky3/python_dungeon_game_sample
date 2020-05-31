import math

from model.chip import Chip


class CharacterChip():

    def __init__(self,
                 dot_size: (int, int),
                 area_size: (int, int),
                 direction_pattern_num: int,
                 animation_pattern_num: int = 2,
                 ):
        self.__chip = Chip(dot_size, area_size)
        self.__character_no = 0
        self.__direction_pattern_num = direction_pattern_num
        self.__animation_pattern_num = animation_pattern_num

    def set_character_no(self, no: int):
        self.__character_no = no

    def get_draw_rect(self,
                      direction_no: int = 0,
                      pattern: int = 0
                      ):

        chip_column = self.__chip.item_size[0]
        anime_pattern_num = self.__animation_pattern_num

        max_oneline_char = chip_column / anime_pattern_num

        character_no = self.__character_no
        char_row = math.floor(character_no / max_oneline_char)
        char_col = character_no % max_oneline_char

        char_detail_row = char_row * self.__direction_pattern_num
        char_datail_col = char_col * anime_pattern_num
        row = (char_detail_row + direction_no) * chip_column
        col = char_datail_col + (pattern % anime_pattern_num)
        index = row + col

        return self.__chip.get_draw_rect(index)
