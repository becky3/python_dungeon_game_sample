from manager.debug_manager import DebugManager


class GameInfo():

    @property
    def floor(self) -> int:
        return self.__floor

    @property
    def hi_score_floor(self) -> int:
        return self.__hi_score_floor

    @property
    def floor_info_view_time(self) -> int:
        return self.__floor_info_view_time

    @property
    def screen_chip_rows(self) -> int:
        return self.__screen_chip_nums[1]

    @property
    def screen_chip_columns(self) -> int:
        return self.__screen_chip_nums[0]

    def __init__(self,
                 map_chip_size: (int, int),
                 screen_chip_nums: (int, int)
                 ):
        super().__init__()
        self.__floor = 1
        self.__hi_score_floor = 1
        self.__floor_info_view_time = 0
        self.__map_chip_size = map_chip_size
        self.__screen_chip_nums = screen_chip_nums

    def reset_floor(self):
        self.__floor = 1
        if DebugManager.is_debug:
            self.__floor = DebugManager.floor

    def add_floor(self):
        self.__floor += 1
        if self.__floor > self.hi_score_floor:
            self.__hi_score_floor = self.__floor

    def set_floor_info_view_time(self, time: int):
        self.__floor_info_view_time = time

    def decrement_floor_info_view_time(self):
        self.__floor_info_view_time -= 1
        if self.__floor_info_view_time <= 0:
            self.__floor_info_view_time = 0

    def convert_map_to_display(self, coordinate: (int, int)) -> (int, int):
        width, height = self.__map_chip_size
        return (coordinate[0] * width, coordinate[1] * height)
