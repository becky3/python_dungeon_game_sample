import math

from model.dungeon import Dungeon
from model.event.player import Player
from model.draw_object.image import Image
from model.draw_object.text import Text
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
                (60, 40),
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

    def draw_parameter(self):  # 主人公の能力を表示
        display_x = 30
        display_y = 600

        game_system = self.game_system
        timer = game_system.timer
        player = self.player

        image = Image(
            "resource/image/parameter.png",
            (display_x, display_y),
            is_absolute_position=True
        )
        game_system.add_draw_object(image)
        col = Color.WHITE
        if player.life < 10 and timer % 2 == 0:
            col = Color.RED
        life_text = "{}/{}".format(player.life, player.max_life)
        game_system.add_draw_object(
            Text(
                life_text,
                (display_x + 128, display_y + 6),
                col,
                Text.FontSize.SMALL
            )
        )
        game_system.add_draw_object(
            Text(
                str(player.strength),
                (display_x + 128, display_y + 33),
                Color.WHITE,
                Text.FontSize.SMALL
            )
        )
        col = Color.WHITE
        if player.food == 0 and timer % 2 == 0:
            col = Color.RED
        game_system.add_draw_object(
            Text(
                str(player.food),
                (display_x + 128, display_y+60),
                col,
                Text.FontSize.SMALL
            )
        )
        game_system.add_draw_object(
            Text(
                str(player.potion),
                (display_x + 266, display_y + 6),
                Color.WHITE,
                Text.FontSize.SMALL
            )
        )
        game_system.add_draw_object(
            Text(
                str(player.blazegem),
                (display_x + 266, display_y+33),
                Color.WHITE,
                Text.FontSize.SMALL
            )
        )
