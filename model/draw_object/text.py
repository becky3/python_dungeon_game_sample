import pygame
from model.draw_object.draw_object import DrawObject


class Text(DrawObject):

    class FontSize:
        NORMAL = 18
        SMALL = 14
        SS = 14

    def __init__(self,
                 text: str,
                 position: (int, int),
                 color: int,
                 font_size: int = FontSize.NORMAL,
                 font_type: str = None,
                 is_absolute_position: bool = True
                 ):
        super().__init__(position, is_absolute_position)
        self.__text = text
        self.__color = color
        self.__font_size = font_size
        self.__font_type = font_type

    def draw(self, display: pygame.display, adjust: (int, int)):
        x = self.x - adjust[0]
        y = self.y - adjust[1]
        font = pygame.font.Font(
            self.__font_type,
            self.__font_size
        )
        text = self.__text

        render = font.render(text, True, (0, 0, 0))
        display.blit(render, [x+1, y+1])

        render = font.render(text, True, self.__color)
        display.blit(render, [x, y])
