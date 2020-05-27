from typing import Optional

from manager.map_manager import MapManager
from manager.sound_manager import SE
from task.task import Task
from const import Color
from model.draw_object.image import Image
from model.draw_object.text import Text
from model.event.treasure_box import TreasureBox
from model.item import Item


class GetTreasureBox(Task):

    def __init__(self, map_manager: MapManager, treasure_box: TreasureBox):
        self.__map_manager = map_manager
        self.__next_task: Task = None
        self.__treasure_box = treasure_box

    def start(self):
        item = self.__treasure_box.get_item()
        se = SE.GOOD_ITEM
        if item.item_type == Item.Type.FOOD_SPOILED:
            se = SE.BAD_ITEM

        mm = self.__map_manager
        mm.game_system.play_se(se)
        mm.player.add_item(item)
        mm.event_manager.remove_treasure(
            self.__treasure_box
        )

    def update(self):
        if self.__map_manager.game_system.timer >= 10:
            from task.map.input_wait import InputWait
            self.__next_task = InputWait(self.__map_manager)

    def draw(self):
        mm = self.__map_manager
        game_system = mm.game_system
        item = self.__treasure_box.get_item()

        mm.draw_map()
        mm.draw_parameter()
        item.draw()

    def exit(self):
        pass

    def get_next_task(self) -> Optional[Task]:
        return self.__next_task
