
import pygame

from model.draw_object.draw_object import DrawObject


class Image(DrawObject):

    @property
    def surface(self) -> pygame.Surface:
        return self.__image

    def __init__(self,
                 file_path: str,
                 position: (int, int) = (0, 0),
                 is_absolute_position: bool = False,
                 area_rect: (int, int, int, int) = None,
                 transform: (float, float) = None
                 ):
        super().__init__(position, is_absolute_position)
        from manager.resource_manager import ResourceManager
        self.__image = ResourceManager.get_image(file_path)
        self.__width, self.__height = self.__image.get_size()
        self.__transform = transform
        self.__area_rect = area_rect

    def draw(self,
             display: pygame.display,
             adjust: (int, int)
             ):
        x, y = adjust

        if self.__transform is None:
            image = self.__image
        else:
            angle, scale = self.__transform
            image = pygame.transform.rotozoom(self.__image, angle, scale)

        display.blit(
            image,
            [self.x - x, self.y - y],
            self.__area_rect
        )
