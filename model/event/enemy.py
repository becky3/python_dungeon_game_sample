from typing import Optional

import random
import math

import numpy

from libs.matrix import Matrix
from const import Direction, Color
from game.game_info import GameInfo
from game.game_system import GameSystem
from model.dungeon import Dungeon, FloorType
from model.item import Item
from model.mover import Mover
from model.character_chip import CharacterChip
from model.event.event import Event
from model.event.player import Player
from model.draw_object.image import Image
from model.draw_object.text import Text
from model.draw_object.rect import Rect
from model.stats import Stats
from manager.debug_manager import DebugManager


class Enemy(Event):

    __IMAGE = "resource/image/enemy.png"
    __MAX_ENEMY_TYPE = 10

    @property
    def stats(self) -> Stats:
        return self.__stats

    @property
    def next_position(self) -> (int, int):
        return self.__next_position

    def __init__(self,
                 position: (int, int),
                 game_system: GameSystem,
                 game_info: GameInfo,
                 dungeon: Dungeon,
                 player: Player,
                 event_map: Matrix,
                 ):

        super().__init__(position)
        self.__dungeon = dungeon
        self.__event_map = event_map
        self.__player = player
        self.__game_system = game_system
        self.__game_info = game_info
        self.__mover = Mover()
        self.__anime_frame = 0
        self.__direction = Direction.NEWTRAL
        self.__next_position: (int, int) = None
        self.__character_chip = CharacterChip(
            (16, 16),
            (16 * 10, 16 * 10),
            direction_pattern_num=1
        )
        self.__anime_frame = 0

        floor = game_info.floor
        start_size = 3
        max_size = math.floor(floor / 3)
        search_size = start_size
        if start_size < max_size:
            search_size = random.randint(start_size, max_size)
        self.__search_size = search_size

        max_enemy_type = math.ceil(floor / 3)
        if max_enemy_type > self.__MAX_ENEMY_TYPE - 1:
            max_enemy_type = self.__MAX_ENEMY_TYPE - 1
        self.type = random.randint(0, max_enemy_type)
        self.__stats = self.__get_default_stats()

        self.__debug_text = "{}".format(self.__stats.max_hp)
        self.__character_chip.set_character_no(self.type)
        self.__damage_view_time = 0

    def __get_default_stats(self) -> Stats:

        floor = self.__game_info.floor
        min_level = math.ceil(floor / 2)
        level = random.randint(min_level, floor)
        max_hp = 60 * \
            (self.type + math.ceil(level / 2)) + \
            (level - 1) * 10
        strength = math.ceil(max_hp / 8)

        return Stats(
            level=level,
            max_hp=max_hp,
            strength=strength
        )

    def __can_move(self, position: (int, int)) -> bool:

        event_map = self.__event_map
        floor_map = self.__dungeon.floor_map

        if not floor_map.is_in(position):
            return False

        y, x = position

        if floor_map[y, x] == FloorType.WALL:
            return False

        if event_map[y, x] is not None:
            return False

        if self.__player.map_coordinate == position:
            return False

        return True

    def __get_next_position(self) -> (int, int):

        reach_y, reach_x = self.__get_player_reach()
        y, x = self.map_coordinate
        if abs(reach_y) <= self.__search_size \
                and abs(reach_x) <= self.__search_size:
            param = (0, 0)
            if abs(reach_x) > abs(reach_y):
                param = (y, x + (numpy.sign(reach_x) * -1))
            else:
                param = (y + (numpy.sign(reach_y) * -1), x)
            return param

        move = random.choice([0, 1])
        new_x = int(x)
        new_y = int(y)
        if move == 0:
            x = new_x + random.choice([-1, 1])
        else:
            y = new_y + random.choice([-1, 1])

        return (y, x)

    def __get_player_reach(self) -> (int, int):
        player_y, player_x = self.__player.map_coordinate
        y, x = self.map_coordinate
        return (y - player_y, x - player_x)

    def battle(self):
        damage = self.__player.stats.strength
        + random.randint(
            1,
            math.floor(self.__player.stats.level * 1.2) + 5
        )
        self.stats.damage(damage)
        self.__damage_view_time = 10

    def get_item(self) -> Optional[Item]:

        if random.random() < 0.8:
            return None

        item_type = random.choice([
            Item.Type.SA_ADD_20,
            Item.Type.SA_ADD_20,
            Item.Type.SA_ADD_20,
            Item.Type.SA_ADD_20,
            Item.Type.SA_ADD_100,
        ])

        return Item(item_type)

    def ready_move(self) -> bool:

        next_position = self.__get_next_position()

        if not self.__can_move(next_position):
            return False

        self.__next_position = next_position
        self.__mover.ready()

        y = next_position[0] - self.map_coordinate[0]
        x = next_position[1] - self.map_coordinate[1]
        self.__direction = (y, x)

        return True

    def __do_move(self):
        self.__anime_frame += 1
        y, x = self.__direction
        value = self.__mover.get_next_plan()
        position = (
            self.y + float(y) * value,
            self.x + float(x) * value
        )
        self.set_position(position)
        if not self.__mover.have_plan():
            self.__moved()

    def __moved(self):
        self.set_position(self.__next_position)
        self.__next_position = None

    def move(self):

        if self.__next_position is None:
            return

        self.__do_move()

    def __draw_bar(self, position: (int, int)):
        game_system = self.__game_system
        width = self.width - 2
        height = 4
        y_adjust = 4
        border_size = 1
        x = position[0] + 1
        y = position[1] - (y_adjust + height)
        max_width = width - border_size * 2
        hp = math.ceil(self.stats.hp / self.stats.max_hp * max_width)
        game_system.add_draw_object(
            Rect(
                (x, y),
                (width, height),
                Color.WHITE
            )
        )
        game_system.add_draw_object(
            Rect(
                (x + border_size, y + border_size),
                (max_width, height - border_size * 2),
                Color.RED
            )
        )
        game_system.add_draw_object(
            Rect(
                (x + border_size, y + border_size),
                (hp, height - border_size * 2),
                Color.GREEN
            )
        )

    def __draw_level(self, position: (int, int)):

        game_system = self.__game_system
        x = position[0]
        y = position[1] + self.height - 8
        text = str(self.stats.level)
        if DebugManager.is_debug:
            text += " " + self.__debug_text

        text1 = Text(
            text,
            (x, y),
            Color.RED,
            font_size=Text.FontSize.SS,
            is_absolute_position=False
        )
        game_system.add_draw_object(text1)

    def __get_animation_image(self) -> Image:
        file_path = self.__IMAGE
        rect = self.__character_chip.get_draw_rect(
            pattern=math.ceil(self.__anime_frame / 2)
        )

        return Image(file_path, area_rect=rect)

    def __draw_damage(self, position: (int, int)):

        game_system = self.__game_system

        adjust = self.__damage_view_time
        x = position[0]
        y = position[1] + self.height - 48 + adjust

        text = Text(
            str(self.stats.pre_damage),
            (x, y),
            Color.WHITE,
            font_size=Text.FontSize.NORMAL,
            is_absolute_position=False
        )
        game_system.add_draw_object(text)

    def draw(self):
        self.__anime_frame += 1
        position = self.__game_info.convert_map_to_display(
            (self.x, self.y)
        )
        image = self.__get_animation_image()
        image.set_position(position)
        self.__game_system.add_draw_object(image)
        self.__draw_level(position)
        self.__draw_bar(position)
        if self.__damage_view_time > 0:
            self.__damage_view_time -= 1
            self.__draw_damage(position)
