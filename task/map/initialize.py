from typing import Optional

from game.game_system import GameSystem
from game.game_info import GameInfo
from task.task import Task
from model.dungeon import Dungeon
from model.event.player import Player
from manager.event_manager import EventManager
from manager.sound_manager import Music
from manager.map_manager import MapManager


class Initialize(Task):

    def __init__(self,
                 game_system: GameSystem,
                 game_info: GameInfo,
                 map_manager: MapManager
                 ):
        self.__game_system = game_system
        self.__game_info = game_info
        self.__map_manager = map_manager
        self.__next_task: Task = None

    def start(self):

        game_system = self.__game_system
        game_info = self.__game_info

        dungeon = Dungeon(
            game_info=game_info,
            base_size=(9, 11),
            room_size=3
        )

        player = Player(
            (0, 0),
            game_system,
            game_info,
            dungeon
        )

        event_manager = EventManager(
            game_system,
            game_info,
            player
        )

        self.__map_manager.set_references(
            game_system,
            game_info,
            dungeon,
            event_manager,
            player
        )

        game_info.reset_floor()
        self.__map_manager.init_floor()

        player.reset_stats()

        game_system.play_music(Music.DUNGEON)

    def update(self):
        from task.map.wait_input import WaitInput
        self.__next_task = WaitInput(self.__map_manager)

    def draw(self):
        pass

    def exit(self):
        pass

    def get_next_task(self) -> Optional[Task]:
        return self.__next_task
