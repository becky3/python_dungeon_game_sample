from typing import Optional

from const import Key
from task.task import Task
from manager.input_manager import InputManager
from manager.title_manager import TitleManager
from manager.sound_manager import SE


class WaitInput(Task):

    def __init__(self, title_manager: TitleManager):
        self.__title_manager = title_manager
        self.__next_task: Task = None

    def start(self):
        self.__next_task = None

    def update(self):
        if not InputManager.isPush(Key.SPACE):
            return

        from task.title.start_effect import StartEffect
        self.__title_manager.game_system.play_se(SE.CHANGE_FLOOR)
        self.__next_task = StartEffect(self.__title_manager)

    def draw(self):
        self.__title_manager.draw_title()

    def exit(self):
        pass

    def get_next_task(self) -> Optional[Task]:
        return self.__next_task
