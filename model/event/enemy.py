import random
import math

import numpy

from libs.matrix import Matrix
from game.game_info import GameInfo
from game.game_system import GameSystem
from model.dungeon import Dungeon
from model.chip import Chip
from model.event.event import Event
from model.event.player import Player
from model.draw_object.image import Image
from model.draw_object.text import Text
from model.draw_object.rect import Rect
from const import Color


class Enemy(Event):

    __IMAGE = "resource/image/enemy.png"
    __CHIP = Chip((16, 16), (16 * 8, 16 * 8))

    __EMY_NAME = [
        "Green slime",
        "Red slime",
        "Axe beast",
        "Ogre",
        "Sword man",
        "Death hornet",
        "Signal slime",
        "Devil plant",
        "Twin killer",
        "Hell"
    ]

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

        floor = game_info.floor
        start_size = 3
        max_size = math.floor(floor / 3)
        search_size = start_size
        if start_size < max_size:
            search_size = random.randint(start_size, max_size)
        self.__search_size = search_size

        self.type = random.randint(0, floor)
        if floor >= 10:
            self.type = random.randint(0, 9)

        self.level = random.randint(1, floor)
        self.name = str(self.level)
        self.max_hp = 60 * (self.type + 1) + (self.level - 1) * 10
        self.hp = self.max_hp
        self.str = int(self.max_hp/8)
        self.__debug_text = "-"

    def __is_move(self, position: (int, int)) -> bool:

        event_map = self.__event_map
        floor_map = self.__dungeon.floor_map

        if not floor_map.is_in(position):
            return False

        y, x = position

        if floor_map[y, x] > 3:
            return False

        if event_map[y, x] is not None:
            return False

        return True

    def __get_move_position(self) -> (int, int):

        reach_y, reach_x = self.__get_player_reach()
        if abs(reach_y) <= self.__search_size and abs(reach_x) <= self.__search_size:
            param = (0, 0)
            if abs(reach_x) > abs(reach_y):
                param = (self.y, self.x + (numpy.sign(reach_x) * -1))
            else:
                param = (self.y + (numpy.sign(reach_y) * -1), self.x)
            return param

        move = random.choice([0, 1])
        x = self.x
        y = self.y
        if move == 0:
            x = self.x + random.choice([-1, 1])
        else:
            y = self.y + random.choice([-1, 1])

        return (y, x)

    def __get_player_reach(self) -> (int, int):
        player_y, player_x = self.__player.map_coordinate
        x = self.x - player_x
        y = self.y - player_y
        return (y, x)

    def damage(self):
        damage = self.__player.strength + self.__player.level
        self.hp -= damage

    def is_die(self) -> bool:
        return self.hp < 0

    def update(self):

        new_position = self.__get_move_position()

        if not self.__is_move(new_position):
            return

        self.set_position(new_position)

    def __draw_bar(self, position: (int, int)):
        game_system = self.__game_system
        width = self.width
        height = 8
        y_adjust = 10
        bs = 2  # border_size
        x = position[0]
        y = position[1] - (y_adjust + height)
        max_width = width - bs * 2
        hp = math.ceil(self.hp / self.max_hp * max_width)
        if hp < 0:
            hp = 0
        game_system.add_draw_object(
            Rect(
                (x, y),
                (width, height),
                Color.WHITE
            )
        )
        game_system.add_draw_object(
            Rect(
                (x + bs, y + bs),
                (max_width, height - bs * 2),
                Color.RED
            )
        )
        game_system.add_draw_object(
            Rect(
                (x + bs, y + bs),
                (hp, height - bs * 2),
                Color.GREEN
            )
        )

    def __draw_level(self, position: (int, int)):

        game_system = self.__game_system
        x = position[0]
        y = position[1] + self.height - 8
        text = self.name
        # text = self.__debug_text

        text1 = Text(
            text,
            (x, y),
            Color.RED,
            font_size=Text.FontSize.SS,
            is_absolute_position=False
        )
        game_system.add_draw_object(text1)

    def __get_image(self, index: int, position: (int, int)) -> Image:
        return Image(
            self.__IMAGE,
            position,
            area_rect=self.__CHIP.get_draw_rect(index)
        )

    def draw(self):

        position = self.__game_info.convert_map_to_display(
            (self.x, self.y)
        )
        image = self.__get_image(0, position)
        self.__game_system.add_draw_object(image)
        self.__draw_level(position)
        self.__draw_bar(position)
