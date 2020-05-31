

from game.game_system import GameSystem
from model.chip import Chip
from model.draw_object.image import Image
from model.draw_object.text import Text
from const import Color


class Item():

    class Type:
        POTION = 0
        BOM = 1
        SA_SPOILED = 2
        SA_ADD_20 = 3
        SA_ADD_100 = 4

    __IMAGE = "resource/image/item.png"
    __CHIP = Chip((16, 16), (16 * 8, 16 * 8))

    __NAMES = [
        "Potion",
        "Bom",
        "SA spoil",
        "SA +20",
        "SA +100",
    ]

    @property
    def item_type(self) -> int:
        return self.__item_type

    def __get_image(self, position: (int, int)) -> Image:
        return Image(
            self.__IMAGE,
            position,
            area_rect=self.__CHIP.get_draw_rect(self.__item_type),
            is_absolute_position=True
        )

    def __init__(self, item_type: int):
        self.__item_type = item_type
        self.__name = self.__NAMES[self.__item_type]

    def draw(self, game_system: GameSystem):

        width, height = game_system.get_screen_size()

        center_x = width / 2
        center_y = height / 2

        image = self.__get_image(
            (center_x - 28, center_y - 36)
        )
        game_system.add_draw_object(image)
        game_system.add_draw_object(
            Text(
                self.__name,
                (center_x - 10, center_y - 32),
                Color.WHITE,
                Text.FontSize.SMALL
            )
        )
