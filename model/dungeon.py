import random
import math
from typing import Callable

from libs.matrix import Matrix
from game.game_system import GameSystem
from game.game_info import GameInfo
from model.draw_object.image import Image
from model.chip import Chip


class FloorPattern:
    FLOOR = 0
    WALL = 1
    WALL2 = 2


class Dungeon:

    __IMAGE = "resource/image/floor.png"
    __CHIP = Chip((16, 16), (16 * 8, 16 * 8))

    def __init__(self,
                 game_info: GameInfo,
                 maze_height: int,
                 maze_width: int,
                 room_size: int,
                 ):
        self.__game_info = game_info
        self.maze = self.__get_maze(maze_height, maze_width)
        self.room_size = room_size
        self.floor_map = Matrix()

    def __get_maze(self, height: int, width: int) -> Matrix:
        maze = Matrix(height, width)

        XP = [0, 1, 0, -1]
        YP = [-1, 0, 1, 0]

        # 周りの壁
        for x in range(width):
            maze[0, x] = 1
            maze[height-1, x] = 1

        for y in range(1, height-1):
            maze[y, 0] = 1
            maze[y, width-1] = 1

        # 中を何もない状態に
        for y in range(1, height-1):
            for x in range(1, width-1):
                maze[y, x] = 0

        # 柱
        for y in range(2, height-2, 2):
            for x in range(2, width-2, 2):
                maze[y, x] = 1

        # 柱から上下左右に壁を作る
        for y in range(2, height-2, 2):
            for x in range(2, width-2, 2):
                d = random.randint(0, 3)
            if x > 2:  # 二列目からは左に壁を作らない
                d = random.randint(0, 2)
            maze[y+YP[d], x+XP[d]] = 1

        return maze

    def create(self):  # ダンジョンの自動生成

        maze = self.maze
        room_size = self.room_size

        maze_height, maze_width = maze.shape
        height = maze_height * room_size
        width = maze_width * room_size

        floor_map = Matrix(height, width)

        # 迷路からダンジョンを作る
        # 全体を壁にする
        for y in range(height):
            for x in range(width):
                floor_map[y, x] = 9
        # 部屋と通路の配置
        for y in range(1, maze_height-1):
            for x in range(1, maze_width-1):
                dx = x*room_size+1
                dy = y*room_size+1
                if maze[y, x] == 0:
                    if random.randint(0, 99) < 20:  # 部屋を作る
                        for ry in range(-1, room_size-1):
                            for rx in range(-1, room_size-1):
                                floor_map[dy+ry, dx+rx] = 0
                    else:  # 通路を作る
                        floor_map[dy, dx] = 0
                        road_size = math.floor(room_size/2) + 1
                        if maze[y-1, x] == 0:
                            for ry in range(1, road_size):
                                floor_map[dy-ry, dx] = 0
                        if maze[y+1, x] == 0:
                            for ry in range(1, road_size):
                                floor_map[dy+ry, dx] = 0
                        if maze[y, x-1] == 0:
                            for rx in range(1, road_size):
                                floor_map[dy, dx-rx] = 0
                        if maze[y, x+1] == 0:
                            for rx in range(1, road_size):
                                floor_map[dy, dx+rx] = 0

        self.floor_map = floor_map

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

        height, width = self.floor_map.shape
        floor_map = self.floor_map
        center_y, center_x = center
        screen_rows = self.__game_info.screen_chip_rows
        screen_columns = self.__game_info.screen_chip_columns
        y_value = math.ceil(screen_rows / 2) + 1
        y_range = range(-y_value, y_value)
        x_value = math.ceil(screen_columns / 2) + 1
        x_range = range(-x_value, x_value)

        game_system.fill_display()
        for around_y in y_range:
            for around_x in x_range:
                map_x = center_x + around_x
                map_y = center_y + around_y
                if 0 <= map_x < width and 0 <= map_y < height:
                    if floor_map[map_y, map_x] <= 3:
                        floor = self.__get_image(
                            FloorPattern.FLOOR,
                            (map_x, map_y)
                        )
                        game_system.add_draw_object(floor)
                    if floor_map[map_y, map_x] == 9:
                        wall2 = self.__get_image(
                            FloorPattern.WALL2,
                            (map_x, map_y)
                        )
                        game_system.add_draw_object(wall2)
                        if map_y < height - 1 and floor_map[map_y+1, map_x] == 9:
                            wall = self.__get_image(
                                FloorPattern.WALL,
                                (map_x, map_y)
                            )
                            game_system.add_draw_object(wall)
