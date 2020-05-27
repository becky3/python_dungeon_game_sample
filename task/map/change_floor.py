from typing import Optional

from manager.map_manager import MapManager
from manager.sound_manager import SE
from task.task import Task
from model.draw_object.rect import Rect


class ChangeFloor(Task):

    def __init__(self, map_manager: MapManager):
        self.__map_manager = map_manager
        self.__next_task: Task = None

    def start(self):
        self.__map_manager.game_system.play_se(
            SE.CHANGE_FLOOR
        )

    def update(self):

        if self.__map_manager.game_system.timer == 10:
            from task.map.input_wait import InputWait
            self.__next_task = InputWait(self.__map_manager)

    def draw(self):
        mm = self.__map_manager
        game_system = mm.game_system
        game_info = mm.game_info
        timer = mm.game_system.timer

        if 1 <= timer <= 5:
            h = 80 * timer
            game_system.add_draw_object(
                Rect((0, 0), (880, h), is_absolute_position=True)
            )
            game_system.add_draw_object(
                Rect((0, 720-h), (880, h), is_absolute_position=True)
            )
        if timer == 5:
            game_info.add_floor()
            mm.game_info.set_welcome_view_time(15)
            mm.init_floor()
        if 6 <= timer <= 9:
            h = 80 * (10 - timer)
            game_system.add_draw_object(
                Rect((0, 0), (880, h), is_absolute_position=True)
            )
            game_system.add_draw_object(
                Rect((0, 720-h), (880, h), is_absolute_position=True)
            )

    def exit(self):
        pass

    def get_next_task(self) -> Optional[Task]:
        return self.__next_task
