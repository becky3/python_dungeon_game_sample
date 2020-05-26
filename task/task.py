from abc import ABC, abstractmethod
from typing import Optional


class Task(ABC):

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
    def get_next_task(self) -> Optional[object]:
        pass
