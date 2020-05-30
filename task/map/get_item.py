from typing import Optional

from manager.map_manager import MapManager
from manager.sound_manager import SE
from task.task import Task
from model.item import Item


class GetItem(Task):

    def __init__(self, map_manager: MapManager, item: Item):
        self.__map_manager = map_manager
        self.__next_task: Task = None
        self.__item = item

    def start(self):
        item = self.__item
        se = SE.GOOD_ITEM
        if item.item_type == Item.Type.SA_SPOILED:
            se = SE.BAD_ITEM

        mm = self.__map_manager
        mm.game_system.play_se(se)
        mm.player.add_item(item)

    def update(self):
        if self.__map_manager.game_system.timer >= 10:
            from task.map.wait_input import WaitInput
            self.__next_task = WaitInput(self.__map_manager)

    def draw(self):
        mm = self.__map_manager
        game_system = mm.game_system

        mm.draw_map()
        mm.draw_parameter()
        self.__item.draw(game_system)

    def exit(self):
        pass

    def get_next_task(self) -> Optional[Task]:
        return self.__next_task
