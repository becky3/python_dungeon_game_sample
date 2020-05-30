import pygame

from manager.sound_manager import SoundManager
from manager.debug_manager import DebugManager
from model.draw_object.draw_object import DrawObject
from model.camera import Camera
from const import Color


class GameSystem():

    @property
    def timer(self) -> int:
        return self.__timer

    @property
    def speed(self) -> int:
        return self.__speed

    @property
    def display(self) -> pygame.display:
        return self.__display

    def __init__(self):
        super().__init__()
        self.__timer = -1
        self.__speed = 1
        self.__display: pygame.display = None
        self.__sound_manager = SoundManager()
        self.__camera: Camera = None

        pygame.init()
        self.__clock = pygame.time.Clock()

    def get_screen_size(self) -> (int, int):
        return self.__camera.screen.get_size()

    def reset_camera(self):
        self.__camera.reset()

    def setup_display(self, size: (int, int), power: int):
        width, height = size
        self.__display = pygame.display.set_mode(
            (width * power, height * power)
        )
        self.__camera = Camera(size, power)

    def set_caption(self, text: str):
        pygame.display.set_caption(text)

    def add_speed(self):
        self.__speed += 1
        if DebugManager.is_debug:
            if self.__speed > 9:
                self.__speed = 1
        elif self.__speed > 4:
            self.__speed = 1

    def reset_timer(self):
        self.__timer = -1

    def progress(self):
        self.__timer += 1

    def update_display(self):
        self.__camera.draw()
        surface = self.__display
        pygame.transform.scale(
            self.__camera.screen,
            surface.get_size(),
            surface
        )
        pygame.display.update()
        self.__clock.tick((self.__speed - 1) * 2 + 8)

    def quit(self):
        pygame.quit()

    def play_music(self, file_path: str):
        self.__sound_manager.play_music(file_path)

    def play_se(self, file_path: str):
        self.__sound_manager.play_se(file_path)

    def stop_music(self):
        self.__sound_manager.stop_music()

    def add_draw_object(self, draw_object: DrawObject):
        self.__camera.add_draw_object(draw_object)

    def fill_display(self, color=Color.BLACK):
        self.__camera.fill(color)

    def add_camera_position(self, position: (int, int)):
        x, y = position
        self.__camera.x += x
        self.__camera.y += y

    def set_camera_position(self, position: (int, int)):
        x, y = position
        self.__camera.x = x
        self.__camera.y = y
