import random

from game.game_system import GameSystem
from game.game_info import GameInfo
from model.item import Item
from model.chip import Chip
from model.event.event import Event
from model.draw_object.image import Image


class TreasureBox(Event):

    __IMAGE = "resource/image/floor.png"
    __CHIP = Chip((16, 16), (16 * 8, 16 * 8))

    def __get_item(self) -> Item:
        item_type = random.choice([
            Item.Type.POTION,
            Item.Type.POTION,
            Item.Type.POTION,
            Item.Type.BOM,
            Item.Type.BOM,
            Item.Type.BOM,
            Item.Type.BOM,
            Item.Type.BOM,
            Item.Type.BOM,
            Item.Type.SA_SPOILED,
        ])
        return Item(item_type)

    def __init__(self,
                 position: (int, int),
                 game_system: GameSystem,
                 game_info: GameInfo
                 ):
        super().__init__(position)
        self.__game_system = game_system
        self.__game_info = game_info
        self.__item = self.__get_item()

    def get_item(self) -> Item:
        return self.__item

    def __get_image(self, index: int, position: (int, int)) -> Image:
        converted_position = self.__game_info.convert_map_to_display(
            position
        )
        return Image(
            self.__IMAGE,
            converted_position,
            area_rect=self.__CHIP.get_draw_rect(index)
        )

    def draw(self):
        image = self.__get_image(3, (self.x, self.y))
        self.__game_system.add_draw_object(image)
