from const import Color
from game.game_system import GameSystem
from model.draw_object.rect import Rect
from model.effect.effect import Effect


class CloseWipe(Effect):

    def __init__(self,
                 game_system: GameSystem,
                 color: int = Color.BLACK,
                 effect_time: int = 10
                 ):
        self.__game_system = game_system
        self.__color = color
        self.__timer = 0
        self.__effect_time = effect_time

    def isEnd(self) -> bool:
        return self.__timer > self.__effect_time

    def update(self):
        self.__timer += 1

    def draw(self):
        game_system = self.__game_system
        one_height = 144 / self.__effect_time
        h = one_height * self.__timer

        game_system.add_draw_object(
            Rect(
                (0, 0),
                (144, h),
                fill_color=self.__color,
                is_absolute_position=True
            )
        )
        game_system.add_draw_object(
            Rect(
                (0, 144 - h),
                (144, h),
                fill_color=self.__color,
                is_absolute_position=True
            )
        )
