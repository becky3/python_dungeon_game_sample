

from game.game_system import GameSystem
from model.chip import Chip
from model.draw_object.image import Image
from model.draw_object.text import Text
from const import Color


class Item():

    class Type:
        POTION = 0
        BLAZE_GEM = 1
        FOOD_SPOILED = 2
        FOOD_ADD_20 = 3
        FOOD_ADD_100 = 4

    __IMAGE = "resource/image/item.png"
    __CHIP = Chip((16, 16), (16 * 8, 16 * 8))

    __NAMES = [
        "Potion",
        "Blaze gem",
        "Food spoiled.",
        "Food +20",
        "Food +100",
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

    def __init__(self,
                 game_system: GameSystem,
                 item_type: int):
        self.__item_type = item_type
        self.__game_system = game_system
        self.__name = self.__NAMES[self.__item_type]

    def draw(self):

        game_system = self.__game_system
        width, height = game_system.get_screen_size()

        center_x = width / 2
        center_y = height / 2

        image = self.__get_image(
            (center_x - 42, center_y - 36)
        )
        self.__game_system.add_draw_object(image)
        self.__game_system.add_draw_object(
            Text(
                self.__name,
                (center_x - 24, center_y - 32),
                Color.WHITE,
                Text.FontSize.SMALL
            )
        )
