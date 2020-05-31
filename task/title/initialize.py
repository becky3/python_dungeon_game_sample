from typing import Optional

from task.task import Task
from manager.sound_manager import Music
from manager.title_manager import TitleManager


class Initialize(Task):

    def __init__(self, title_manager: TitleManager):
        self.__title_manager = title_manager
        self.__next_task: Task = None

    def start(self):
        game_system = self.__title_manager.game_system
        game_system.play_music(Music.TITLE)
        game_system.reset_camera()

    def update(self):
        from task.title.wait_input import WaitInput
        self.__next_task = WaitInput(self.__title_manager)

    def draw(self):
        pass

    def exit(self):
        pass

    def get_next_task(self) -> Optional[Task]:
        return self.__next_task
