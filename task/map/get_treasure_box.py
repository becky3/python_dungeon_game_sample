from typing import Optional

from manager.map_manager import MapManager
from task.task import Task
from const import Color
from model.draw_object.image import Image
from model.draw_object.text import Text
from model.event.treasure_box import TreasureBox


class GetTreasureBox(Task):

    def __init__(self, map_manager: MapManager, treasure_box: TreasureBox):
        self.__map_manager = map_manager
        self.__next_task: Task = None
        self.__treasure_box = treasure_box

    def start(self):
        self.__map_manager.player.add_item(
            self.__treasure_box.get_item()
        )
        self.__map_manager.event_manager.remove_treasure(
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
        image = Image(
            item.image_file_path,
            (320, 220),
            is_absolute_position=True
        )
        game_system.add_draw_object(image)
        game_system.add_draw_object(
            Text(
                item.name,
                (380, 240),
                Color.WHITE,
                Text.FontSize.SMALL
            )
        )

    def exit(self):
        pass

    def get_next_task(self) -> Optional[Task]:
        return self.__next_task
