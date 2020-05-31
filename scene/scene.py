from abc import ABC, abstractmethod
from typing import Optional

from game.game_system import GameSystem
from game.game_info import GameInfo
from task.task import Task
from manager.debug_manager import DebugManager


class Scene(ABC):

    @property
    def game_system(self) -> GameSystem:
        return self.__game_system

    @property
    def game_info(self) -> GameInfo:
        return self.__game_info

    @property
    def task(self) -> Task:
        return self.__task

    def __init__(self,
                 game_system: GameSystem,
                 game_info: GameInfo,
                 task: Task):
        self.__game_system = game_system
        self.__game_info = game_info
        self.__task = task

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self):

        game_system = self.__game_system
        task = self.__task

        if game_system.timer == 0:
            DebugManager.print("new task:" + task.__class__.__name__)
            task.start()
            return

        task.update()

        next_task = task.get_next_task()
        if next_task is not None:
            task.draw()
            task.exit()
            DebugManager.print("end task:" + task.__class__.__name__)
            self.__task = next_task
            game_system.reset_timer()

    @abstractmethod
    def draw(self):
        self.__task.draw()

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def get_next_scene(self) -> Optional[object]:
        pass
