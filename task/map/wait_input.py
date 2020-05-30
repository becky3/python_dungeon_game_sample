from typing import Optional

from const import Key, Direction

from manager.map_manager import MapManager
from manager.input_manager import InputManager
from manager.sound_manager import SE
from task.task import Task
from model.item import Item


class WaitInput(Task):

    def __init__(self, map_manager: MapManager):
        self.__map_manager = map_manager
        self.__next_task = None

    def __isPush(self, key: int) -> bool:
        return InputManager.isPush(key)

    def start(self):
        pass

    def update(self):
        mm = self.__map_manager
        player = mm.player
        game_system = mm.game_system

        if InputManager.isPush(Key.s):
            game_system.add_speed()

        if InputManager.isPush(Key.p) \
                and player.stats.potion > 0:
            from task.map.use_item import UseItem
            self.__next_task = UseItem(
                self.__map_manager, Item(Item.Type.POTION)
            )
            return

        if InputManager.isPush(Key.b) \
                and player.stats.bom > 0:
            from task.map.use_item import UseItem
            self.__next_task = UseItem(
                self.__map_manager, Item(Item.Type.BOM)
            )
            return

        direction = InputManager.get_push_direction()
        if player.ready_move(direction):
            mm.event_manager.ready_move_enemys()
            from task.map.move import Move
            self.__next_task = Move(self.__map_manager)
            return
        elif direction != Direction.NEWTRAL:
            game_system.play_se(SE.BUMP)

    def draw(self):
        mm = self.__map_manager
        mm.draw_map()
        mm.draw_parameter()
        mm.draw_floor_info()

    def exit(self):
        pass

    def get_next_task(self) -> Optional[Task]:
        return self.__next_task
