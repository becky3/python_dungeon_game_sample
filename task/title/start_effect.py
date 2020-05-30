from typing import Optional

from task.task import Task
from manager.title_manager import TitleManager
from model.effect.close_wipe import CloseWipe


class StartEffect(Task):

    def __init__(self, title_manager: TitleManager):
        self.__title_manager = title_manager
        self.__next_task: Task = None
        self.__effect = CloseWipe(title_manager.game_system)

    def start(self):
        pass

    def update(self):
        self.__effect.update()
        if self.__effect.isEnd():
            from task.title.scene_to_map import SceneToMap
            self.__next_task = SceneToMap()

    def draw(self):
        self.__title_manager.draw_title()
        self.__effect.draw()

    def exit(self):
        pass

    def get_next_task(self) -> Optional[Task]:
        return self.__next_task
