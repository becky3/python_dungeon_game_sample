from typing import Optional

from manager.map_manager import MapManager
from task.task import Task
from const import Color, Direction
from manager.sound_manager import Music
from model.draw_object.text import Text
from model.event.player import Player


class GameOver(Task):

    def __init__(self, map_manager: MapManager):
        self.__map_manager = map_manager
        self.__next_task: Task = None

    def start(self):
        self.__map_manager.game_system.stop_music()

    def update(self):

        if self.__map_manager.game_system.timer == 100:
            from task.map.scene_to_title import SceneToTitle
            self.__next_task = SceneToTitle()

    def draw(self):
        mm = self.__map_manager
        game_system = mm.game_system
        timer = game_system.timer
        player = mm.player

        if timer < 30:
            PL_TURN = [
                Direction.UP,
                Direction.RIGHT,
                Direction.DOWN,
                Direction.LEFT,
            ]
            player.set_direction(PL_TURN[timer % 4])

        elif timer == 30:
            player.set_character_type(Player.CharacterType.DIE)
            game_system.play_music(Music.GAME_OVER)

        mm.draw_map()
        mm.draw_parameter()

        if timer > 30:
            game_system.add_draw_object(
                Text(
                    "You died.",
                    (46, 40),
                    Color.YELLOW,
                    Text.FontSize.SMALL
                )
            )
            game_system.add_draw_object(
                Text(
                    "Game over.",
                    (46, 80),
                    Color.YELLOW,
                    Text.FontSize.SMALL
                )
            )

    def exit(self):
        pass

    def get_next_task(self) -> Optional[Task]:
        return self.__next_task
