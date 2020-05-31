import random
import math

from libs.matrix import Matrix
from game.game_system import GameSystem
from game.game_info import GameInfo
from model.draw_object.image import Image
from model.chip import Chip


class FloorType:
    FLOOR = 0
    WALL = 9


class Dungeon:

    __IMAGE = "resource/image/floor.png"
    __CHIP = Chip((16, 16), (16 * 8, 16 * 8))

    class FloorImageType:
        FLOOR = 0
        WALL1 = 1
        WALL2 = 2

    @property
    def floor_map(self) -> Matrix:
        return self.__floor_map

    @property
    def room_size(self) -> int:
        return self.__room_size

    def __init__(self,
                 game_info: GameInfo,
                 base_size: (int, int),
                 room_size: int
                 ):
        self.__game_info = game_info
        self.__base_size = base_size
        self.__room_size = room_size
        self.__floor_map = Matrix()

    def __get_base_map(self) -> Matrix:
        height, width = self.__base_size
        base_map = Matrix(height, width)

        XP = [0, 1, 0, -1]
        YP = [-1, 0, 1, 0]

        FLOOR = FloorType.FLOOR
        WALL = FloorType.WALL

        for x in range(width):
            base_map[0, x] = WALL
            base_map[height-1, x] = WALL

        for y in range(1, height-1):
            base_map[y, 0] = WALL
            base_map[y, width-1] = WALL

        for y in range(1, height-1):
            for x in range(1, width-1):
                base_map[y, x] = FLOOR

        for y in range(2, height-2, 2):
            for x in range(2, width-2, 2):
                base_map[y, x] = WALL

        for y in range(2, height-2, 2):
            for x in range(2, width-2, 2):
                d = random.randint(0, 3)
            if x > 2:
                d = random.randint(0, 2)
            base_map[y+YP[d], x+XP[d]] = WALL

        return base_map

    def create_floor_map(self):

        base_size = self.__base_size
        room_size = self.__room_size
        base_map = self.__get_base_map()

        base_height, base_width = base_size
        height = base_height * room_size
        width = base_width * room_size

        floor_map = Matrix(height, width)

        FLOOR = FloorType.FLOOR
        WALL = FloorType.WALL

        for y in range(height):
            for x in range(width):
                floor_map[y, x] = WALL

        for y in range(1, base_height-1):
            for x in range(1, base_width-1):
                dx = x*room_size+1
                dy = y*room_size+1
                if base_map[y, x] == FLOOR:
                    if random.randint(0, 99) < 20:
                        for ry in range(-1, room_size-1):
                            for rx in range(-1, room_size-1):
                                floor_map[dy+ry, dx+rx] = FLOOR
                    else:
                        floor_map[dy, dx] = FLOOR
                        road_size = math.floor(room_size/2) + 1
                        if base_map[y-1, x] == FLOOR:
                            for ry in range(1, road_size):
                                floor_map[dy-ry, dx] = FLOOR
                        if base_map[y+1, x] == FLOOR:
                            for ry in range(1, road_size):
                                floor_map[dy+ry, dx] = FLOOR
                        if base_map[y, x-1] == FLOOR:
                            for rx in range(1, road_size):
                                floor_map[dy, dx-rx] = FLOOR
                        if base_map[y, x+1] == FLOOR:
                            for rx in range(1, road_size):
                                floor_map[dy, dx+rx] = FLOOR

        self.__floor_map = floor_map

    def __get_image(self, index: int, position: (int, int)) -> Image:
        converted_position = self.__game_info.convert_map_to_display(
            position
        )
        return Image(
            self.__IMAGE,
            converted_position,
            area_rect=self.__CHIP.get_draw_rect(index)
        )

    def draw(self,
             game_system: GameSystem,
             center: (int, int)
             ):

        height, width = self.__floor_map.shape
        floor_map = self.__floor_map
        center_y, center_x = center
        screen_rows = self.__game_info.screen_chip_rows
        screen_columns = self.__game_info.screen_chip_columns
        y_value = math.ceil(screen_rows / 2) + 1
        y_range = range(-y_value, y_value)
        x_value = math.ceil(screen_columns / 2) + 1
        x_range = range(-x_value, x_value)

        WALL = FloorType.WALL
        FLOOR = FloorType.FLOOR

        game_system.fill_display()
        for around_y in y_range:
            for around_x in x_range:
                map_x = center_x + around_x
                map_y = center_y + around_y
                if not floor_map.is_in((map_y, map_x)):
                    continue

                if floor_map[map_y, map_x] == FLOOR:
                    floor = self.__get_image(
                        Dungeon.FloorImageType.FLOOR,
                        (map_x, map_y)
                    )
                    game_system.add_draw_object(floor)

                if floor_map[map_y, map_x] == WALL:
                    wall2 = self.__get_image(
                        Dungeon.FloorImageType.WALL2,
                        (map_x, map_y)
                    )
                    game_system.add_draw_object(wall2)
                    if map_y < height - 1 \
                            and floor_map[map_y+1, map_x] == WALL:
                        wall = self.__get_image(
                            Dungeon.FloorImageType.WALL1,
                            (map_x, map_y)
                        )
                        game_system.add_draw_object(wall)
