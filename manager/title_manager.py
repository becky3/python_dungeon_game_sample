
from model.draw_object.text import Text
from model.draw_object.image import Image
from game.game_info import GameInfo
from game.game_system import GameSystem
from const import Color


class TitleManager:

    __BLINK = [
        (224, 255, 255),
        (192, 240, 255),
        (128, 224, 255),
        (64, 192, 255),
        (128, 224, 255),
        (192, 240, 255)
    ]

    @property
    def game_system(self) -> GameSystem:
        return self.__game_system

    @property
    def game_info(self) -> GameInfo:
        return self.__game_info

    def __init__(self, game_system: GameSystem, game_info: GameInfo):
        self.__game_system: GameSystem = game_system
        self.__game_info: GameInfo = game_info

    def draw_title(self):

        game_system = self.__game_system
        game_info = self.__game_info

        hi_score_floor = game_info.hi_score_floor
        timer = game_system.timer

        game_system.fill_display()
        width, height = game_system.get_screen_size()

        title_x = width / 2 - 64
        title_y = height / 2 - 32

        image = Image("resource/image/title.png", (title_x, title_y))
        game_system.add_draw_object(image)

        if hi_score_floor >= 2:
            floor_text = "HI SCORE : B {} F".format(hi_score_floor)
            game_system.add_draw_object(
                Text(
                    floor_text,
                    (8, 8),
                    Color.CYAN
                )
            )
        game_system.add_draw_object(
            Text(
                "Press space key",
                (24, 112),
                self.__BLINK[timer % 6]
            )
        )
