from typing import Optional

from manager.map_manager import MapManager
from manager.sound_manager import SE
from task.task import Task
from model.effect.close_wipe import CloseWipe


class ChangeFloor(Task):

    def __init__(self, map_manager: MapManager):
        self.__map_manager = map_manager
        self.__next_task: Task = None
        self.__effect = CloseWipe(map_manager.game_system)

    def start(self):
        self.__map_manager.game_system.play_se(
            SE.CHANGE_FLOOR
        )

    def update(self):
        self.__effect.update()
        if self.__effect.isEnd():
            from task.map.wait_input import WaitInput
            self.__next_task = WaitInput(self.__map_manager)

    def draw(self):
        self.__effect.draw()

    def exit(self):
        mm = self.__map_manager
        mm.game_info.add_floor()
        mm.init_floor()

    def get_next_task(self) -> Optional[Task]:
        return self.__next_task
