from typing import Optional

from manager.map_manager import MapManager
from task.task import Task
from const import Color, Direction
from manager.sound_manager import Music, SE
from model.draw_object.text import Text


class LevelUp(Task):

    def __init__(self, map_manager: MapManager):
        self.__map_manager = map_manager
        self.__next_task: Task = None

    def start(self):
        mm = self.__map_manager
        mm.game_system.stop_music()
        mm.game_system.play_se(
            SE.LEVEL_UP
        )
        mm.player.stats.level_up()
        mm.player.set_direction(Direction.DOWN)

    def update(self):

        if self.__map_manager.game_system.timer == 30:
            from task.map.wait_input import WaitInput
            self.__next_task = WaitInput(self.__map_manager)

    def draw(self):
        mm = self.__map_manager
        game_system = mm.game_system
        timer = game_system.timer

        mm.draw_map()
        mm.draw_parameter()

        if timer > 5:
            game_system.add_draw_object(
                Text(
                    "LEVEL UP!!",
                    (40, 40),
                    Color.GREEN,
                    Text.FontSize.NORMAL
                )
            )

    def exit(self):
        mm = self.__map_manager
        mm.game_system.stop_music()
        mm.game_system.play_music(
            Music.DUNGEON
        )

    def get_next_task(self) -> Optional[Task]:
        return self.__next_task
