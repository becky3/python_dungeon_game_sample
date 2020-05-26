from abc import ABC, abstractmethod
from typing import Optional

from game.game_system import GameSystem
from game.game_info import GameInfo


class Scene(ABC):

    @property
    def game_system(self) -> GameSystem:
        return self.__game_sytem

    @property
    def game_info(self) -> GameInfo:
        return self.__agme_info

    def __init__(self):
        self.__game_sytem: GameSystem = None
        self.__agme_info: GameInfo = None

    def initialize(self, game_system: GameSystem, game_info: GameInfo):
        self.__game_sytem = game_system
        self.__agme_info = game_info

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def get_next_scene(self) -> Optional[object]:
        pass
