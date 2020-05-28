from typing import Optional

from manager.map_manager import MapManager
from task.task import Task
from const import Color, Direction
from manager.sound_manager import SE
from model.draw_object.text import Text


class LevelUp(Task):

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

        if timer < 8:
            PL_TURN = [
                Direction.UP,
                Direction.RIGHT,
                Direction.DOWN,
                Direction.LEFT,
            ]
            player.set_direction(PL_TURN[timer % 4])
            if timer == 8:
                player.set_direction(Direction.DOWN)
            mm.draw_map()
            mm.draw_parameter()
        elif timer == 10:
            game_system.play_se(SE.LEVEL_UP)
            game_system.add_draw_object(
                Text(
                    "You died.",
                    (360, 240),
                    Color.RED,
                    Text.FontSize.SMALL
                )
            )
            game_system.add_draw_object(
                Text(
                    "Game over.",
                    (360, 380),
                    Color.RED,
                    Text.FontSize.SMALL
                )
            )

    def exit(self):
        pass

    def get_next_task(self) -> Optional[Task]:
        return self.__next_task
