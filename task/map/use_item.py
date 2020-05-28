from typing import Optional

from manager.map_manager import MapManager
from task.task import Task
from manager.sound_manager import SE
from model.item import Item


class UseItem(Task):

    def __init__(self, map_manager: MapManager, item: Item):
        self.__map_manager = map_manager
        self.__next_task: Task = None
        self.__item = item

    def start(self):
        mm = self.__map_manager
        item = self.__item
        se: str

        if item.item_type == Item.Type.POTION:
            se = SE.POTION
        elif item.item_type == Item.Type.BOM:
            se = SE.BOM

        mm.player.use_item(item)
        mm.game_system.play_se(se)

    def update(self):

        item_type = self.__item.item_type
        if item_type == Item.Type.POTION:
            self.__potion_update()
        elif item_type == Item.Type.BOM:
            self.__bom_update()

    def __potion_update(self):
        if self.__map_manager.game_system.timer == 10:
            from task.map.input_wait import InputWait
            self.__next_task = InputWait(self.__map_manager)

    def __bom_upadte(self):
        pass

    def draw(self):

        item_type = self.__item.item_type
        if item_type == Item.Type.POTION:
            self.__potion_update()
        elif item_type == Item.Type.BOM:
            self.__bom_update()

        mm = self.__map_manager
        mm.draw_map()
        mm.draw_parameter()

    def __potion_draw(self):
        pass

    def __bom_draw(self):
        pass

    def exit(self):
        pass

    def get_next_task(self) -> Optional[Task]:
        return self.__next_task
