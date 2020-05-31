import math

from model.dungeon import Dungeon
from model.event.player import Player
from model.draw_object.text import Text
from model.draw_object.rect import Rect
from manager.event_manager import EventManager
from game.game_info import GameInfo
from game.game_system import GameSystem
from const import Color


class MapManager:

    @property
    def game_system(self) -> GameSystem:
        return self.__game_system

    @property
    def game_info(self) -> GameInfo:
        return self.__game_info

    @property
    def dungeon(self) -> Dungeon:
        return self.__dungeon

    @property
    def event_manager(self) -> EventManager:
        return self.__event_manager

    @property
    def player(self) -> Player:
        return self.__player

    def __init__(self):
        self.__game_system = None
        self.__game_info = None
        self.__dungeon = None
        self.__event_manager = None
        self.__player = None

    def set_references(self,
                       game_system: GameSystem,
                       game_info: GameInfo,
                       dungeon: Dungeon,
                       event_manager: EventManager,
                       player: Player
                       ):
        self.__game_system = game_system
        self.__game_info = game_info
        self.__dungeon = dungeon
        self.__event_manager = event_manager
        self.__player = player

    def init_floor(self):
        self.dungeon.create_floor_map()
        self.player.setup_start_position()
        self.event_manager.create_events(self.dungeon)
        self.game_info.set_floor_info_view_time(10)

    def draw_floor_info(self):

        game_system = self.game_system
        game_info = self.__game_info

        floor_text = "({},{})".format(
            self.player.map_coordinate[0],
            self.player.map_coordinate[1]
        )

        game_system.add_draw_object(
            Text(
                floor_text,
                (8, 8),
                Color.WHITE,
                Text.FontSize.SMALL
            )
        )

        speed_text = "[S]peed "+str(game_system.speed)
        game_system.add_draw_object(
            Text(
                speed_text,
                (100, 8),
                Color.WHITE,
                Text.FontSize.SMALL
            )
        )
        if game_info.floor_info_view_time <= 0:
            return

        game_info.decrement_floor_info_view_time()
        floor_info_text = "B {} F".format(game_info.floor)
        game_system.add_draw_object(
            Text(
                floor_info_text,
                (56, 40),
                Color.CYAN
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
            "LV {}".format(player.stats.level),
            "STR {}".format(player.stats.strength)
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

        stats = self.player.stats

        texts = [
            "HP {}/{}".format(stats.hp, stats.max_hp),
            "SA {}".format(stats.satiation)
        ]

        text = " ".join(texts)
        color = Color.WHITE
        if stats.hp / stats.max_hp < 0.2 or stats.hp <= 10:
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

        stats = self.player.stats

        self.game_system.add_draw_object(
            Text(
                "[ P ] {}".format(stats.potion),
                (x, y),
                Color.GREEN,
                Text.FontSize.SMALL
            )
        )

        self.game_system.add_draw_object(
            Text(
                "[ B ] {}".format(stats.bom),
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
