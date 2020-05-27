import math

from model.dungeon import Dungeon
from model.event.player import Player
from model.draw_object.image import Image
from model.draw_object.text import Text
from model.draw_object.rect import Rect
from manager.event_manager import EventManager
from game.game_info import GameInfo
from game.game_system import GameSystem
from const import Color


class MapManager:

    def __init__(self,
                 game_system: GameSystem,
                 game_info: GameInfo,
                 dungeon: Dungeon,
                 event_manager: EventManager,
                 player: Player
                 ):
        self.game_system = game_system
        self.game_info = game_info
        self.dungeon = dungeon
        self.event_manager = event_manager
        self.player = player

    def init_floor(self):
        dungeon = self.dungeon
        dungeon.create()
        self.player.setup_start_position()
        self.event_manager.create_events(dungeon)

    def draw_floor_info(self):
        floor_text = "floor {} ({},{})".format(
            self.game_info.floor,
            self.player.x,
            self.player.y
        )

        self.game_system.add_draw_object(
            Text(
                floor_text,
                (8, 8),
                Color.WHITE,
                Text.FontSize.SMALL
            )
        )

    def draw_map(self):
        converter = self.game_info.convert_map_to_display
        x = self.player.x - math.floor(self.game_info.screen_chip_columns / 2)
        y = self.player.y - math.floor(self.game_info.screen_chip_rows / 2)
        position = converter((x, y))
        self.game_system.set_camera_position(position)

        center = self.player.map_coordinate
        dungeon = self.dungeon
        game_system = self.game_system

        self.dungeon.draw(game_system, center)
        self.event_manager.draw(
            game_system,
            center,
            dungeon.floor_map
        )
        self.player.draw()

    def __draw_floor_info(self, base_position: (int, int)):

        x, y = base_position
        floor = self.game_info.floor
        player = self.player

        texts = [
            "B{}F".format(floor),
            "LV {}".format(player.level),
        ]

        text = "  ".join(texts)

        self.game_system.add_draw_object(
            Text(
                text,
                (x, y),
                Color.CYAN,
                Text.FontSize.SMALL
            )
        )

    def __draw_player_info(self, base_position: (int, int)):

        x, y = base_position

        timer = self.game_system.timer
        player = self.player

        texts = [
            "HP {}/{}".format(player.hp, player.max_hp),
            "SA {}".format(player.satiation)
        ]

        text = " ".join(texts)
        color = Color.WHITE
        if player.hp / player.max_hp < 0.2 or player.hp <= 10:
            color = Color.RED

        self.game_system.add_draw_object(
            Text(
                text,
                (x, y + 12),
                color,
                Text.FontSize.SMALL
            )
        )

    def __draw_item_info(self, base_position: (int, int)):

        x = base_position[0] + 96
        y = base_position[1]

        player = self.player

        self.game_system.add_draw_object(
            Text(
                "[ P ] {}".format(player.potion),
                (x, y),
                Color.GREEN,
                Text.FontSize.SMALL
            )
        )

        self.game_system.add_draw_object(
            Text(
                "[ F ] {}".format(player.blazegem),
                (x, y + 12),
                Color.GREEN,
                Text.FontSize.SMALL
            )
        )

    def draw_parameter(self):

        base_x = 8
        base_y = 120
        base_position = (base_x, base_y)

        game_system = self.game_system

        game_system.add_draw_object(
            Rect(
                (0, base_y - 2),
                (144, 144 - base_y + 2),
                is_absolute_position=True
            )
        )

        self.__draw_floor_info(base_position)
        self.__draw_player_info(base_position)
        self.__draw_item_info(base_position)
