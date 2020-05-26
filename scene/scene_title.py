from const import Color, Key
from scene.scene import Scene
from scene.scene_map import SceneMap
from manager.input_manager import InputManager
from manager.sound_manager import Music
from model.draw_object.image import Image
from model.draw_object.text import Text


class SceneTitle(Scene):

    __BLINK = [
        (224, 255, 255),
        (192, 240, 255),
        (128, 224, 255),
        (64, 192, 255),
        (128, 224, 255),
        (192, 240, 255)
    ]

    def __init__(self):
        super().__init__()
        self.__next_scene: Scene = None

    def start(self):
        super().game_system.play_music(Music.TITLE)
        super().game_system.reset_camera()

    def update(self):
        if InputManager.isPush(Key.SPACE):
            self.__next_scene = SceneMap()

    def draw(self):
        hi_score_floor = super().game_info.hi_score_floor
        timer = super().game_system.timer

        game_system = super().game_system
        game_system.fill_display()
        width, height = game_system.get_screen_size()

        title_x = width / 2 - 64
        title_y = height / 2 - 32

        image = Image("resource/image/title.png", (title_x, title_y))
        game_system.add_draw_object(image)

        if hi_score_floor >= 2:
            floor_text = "You reached floor {}.".format(hi_score_floor)
            game_system.add_draw_object(
                Text(
                    floor_text,
                    (30, 46),
                    Color.CYAN
                )
            )
        game_system.add_draw_object(
            Text(
                "Press space key",
                (320, 560),
                self.__BLINK[timer % 6]
            )
        )

    def exit(self):
        print("title end")

    def get_next_scene(self):
        return self.__next_scene
