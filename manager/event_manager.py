import random
import math
from typing import Optional

from libs.matrix import Matrix
from game.game_system import GameSystem
from game.game_info import GameInfo
from model.event.event import Event
from model.event.enemy import Enemy
from model.event.treasure_box import TreasureBox
from model.event.stairs import Stairs
from model.event.player import Player
from model.dungeon import Dungeon, FloorType


class EventManager:

    @property
    def enemys(self) -> []:
        return self.__enemy_map.get_not_empty_values()

    @property
    def enemy_map(self) -> Matrix:
        return self.__enemy_map

    @property
    def treasure_map(self) -> Matrix:
        return self.__treasure_map

    def __init__(self,
                 game_system: GameSystem,
                 game_info: GameInfo,
                 player: Player
                 ):
        self.__game_system = game_system
        self.__game_info = game_info
        self.__player = player
        self.__enemy_map = Matrix()
        self.__treasure_map = Matrix()
        self.__stair: Stairs = None

    def remove_enemy(self, event: Event):
        self.__enemy_map[event.map_coordinate] = None

    def remove_treasure(self, treasure_box: TreasureBox):
        self.__treasure_map[treasure_box.map_coordinate] = None

    def all_reset_events(self):
        self.__enemy_map = Matrix()
        self.__treasure_map = Matrix()

    def ready_move_enemys(self):
        for enemy in self.__enemy_map.get_not_empty_values():
            if not enemy.ready_move():
                continue
            self.__enemy_map[enemy.next_position] = enemy
            self.__enemy_map[enemy.map_coordinate] = None

    def move_enemys(self):
        for enemy in self.__enemy_map.get_not_empty_values():
            enemy.move()

    def get_enemy(self, position: (int, int)) -> Optional[Enemy]:
        return self.__enemy_map[position]

    def get_treasure_box(self, position: (int, int)) -> Optional[TreasureBox]:
        return self.__treasure_map[position]

    def is_floor_clear(self) -> bool:
        return self.__player.map_coordinate == self.__stair.map_coordinate

    def __create_stair(self,
                       floor_map: Matrix,
                       width: int,
                       height: int,
                       room_size: int):
        while True:
            x = random.randint(3, width - 4)
            y = random.randint(3, height - 4)
            if floor_map[y, x] == FloorType.WALL:
                continue
            area_size = math.floor(room_size / 2) + 1
            for ry in range(-area_size, area_size):
                for rx in range(-area_size, area_size):
                    floor_map[y+ry, x+rx] = FloorType.FLOOR
            self.__stair = Stairs((y, x), self.__game_system, self.__game_info)
            break

    def __can_create_events(self,
                            dungeon: Dungeon,
                            position: (int, int)) -> bool:
        y, x = position
        if dungeon.floor_map[y, x] == FloorType.WALL:
            return False
        if self.__enemy_map[y, x] is not None:
            return False
        if self.__treasure_map[y, x] is not None:
            return False
        if self.__stair.y == y and self.__stair.x == x:
            return False
        return True

    def create_events(self, dungeon: Dungeon):

        self.all_reset_events()

        floor_map = dungeon.floor_map
        room_size = dungeon.room_size
        player = self.__player

        height, width = floor_map.shape

        self.__enemy_map = Matrix(height, width, dtype="object")
        self.__treasure_map = Matrix(height, width, dtype="object")

        self.__create_stair(floor_map, width, height, room_size)

        for _ in range(60):
            x = random.randint(3, width - 4)
            y = random.randint(3, height - 4)
            if not self.__can_create_events(dungeon, (y, x)):
                continue
            choice = random.choice([1, 2, 2, 2, 2])
            if choice == 1:
                treasure = TreasureBox(
                    (y, x),
                    self.__game_system,
                    self.__game_info
                )
                self.__treasure_map[
                    treasure.map_coordinate
                ] = treasure

            else:
                enemy = Enemy(
                    (y, x),
                    self.__game_system,
                    self.__game_info,
                    dungeon,
                    player,
                    self.__enemy_map
                )
                self.__enemy_map[
                    enemy.map_coordinate
                ] = enemy

    def draw(self,
             game_system: GameSystem,
             center: (int, int),
             floor_map: Matrix
             ):

        center_y, center_x = center

        min_y = -4
        max_y = 6
        min_x = -5
        max_x = 6

        self.__stair.draw()

        for around_y in range(min_y, max_y):
            for around_x in range(min_x, max_x):
                map_y = center_y + around_y
                map_x = center_x + around_x
                if not floor_map.is_in((map_y, map_x)):
                    continue

                treasure = self.__treasure_map[map_y, map_x]
                if treasure is not None:
                    treasure.draw()

                enemy = self.__enemy_map[map_y, map_x]
                if enemy is not None:
                    enemy.draw()
