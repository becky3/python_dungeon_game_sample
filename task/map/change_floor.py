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
        mm = self.__map_manager
        mm.game_system.play_se(
            SE.CHANGE_FLOOR
        )
        mm.game_info.add_floor()
        mm.init_floor()

    def update(self):

        if self.__map_manager.game_system.timer == 10:
            from task.map.wait_input import WaitInput
            self.__next_task = WaitInput(self.__map_manager)

    def draw(self):
        mm = self.__map_manager
        game_system = mm.game_system
        timer = mm.game_system.timer
        one_height = 144 / 10

        if 1 <= timer <= 5:
            h = one_height * timer
            game_system.add_draw_object(
                Rect((0, 0), (144, h), is_absolute_position=True)
            )
            game_system.add_draw_object(
                Rect((0, 144-h), (144, h), is_absolute_position=True)
            )
        if timer == 5:
            mm.game_info.set_floor_info_view_time(15)
        if 6 <= timer <= 9:
            h = one_height * (10 - timer)
            game_system.add_draw_object(
                Rect((0, 0), (144, h), is_absolute_position=True)
            )
            game_system.add_draw_object(
                Rect((0, 144-h), (144, h), is_absolute_position=True)
            )

    def exit(self):
        pass

    def get_next_task(self) -> Optional[Task]:
        return self.__next_task
