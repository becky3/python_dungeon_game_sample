from const import Color
from model.dungeon import Dungeon
from model.draw_object.text import Text
from model.event.player import Player
from manager.event_manager import EventManager
from manager.sound_manager import Music
from manager.map_manager import MapManager
from scene.scene import Scene
from task.task import Task
from task.map.input_wait import InputWait
from task.map.scene_to_title import SceneToTitle


class SceneMap(Scene):

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
        self.__next_scene = None
        self.__task: Task = None
        self.__map_manager = None

    def start(self):

        # TODO: この辺の処理は初期化タスクでやりたい
        game_system = super().game_system
        game_info = super().game_info

        dungeon = Dungeon(
            game_info=game_info,
            maze_height=9,
            maze_width=11,
            room_size=3
        )

        player = Player(
            (0, 0),
            game_system,
            game_info,
            dungeon
        )

        event_manager = EventManager(
            game_system,
            game_info,
            player
        )

        self.__map_manager = MapManager(
            game_system,
            game_info,
            dungeon,
            event_manager,
            player
        )

        self.__map_manager.init_floor()
        game_info.reset_floor()

        player.reset_status()
        player.set_event_map(event_manager.enemy_map)

        game_system.play_music(Music.DUNGEON)

        self.__task = InputWait(self.__map_manager)

    def update(self):
        from scene.scene_title import SceneTitle

        self.__task.update()

        next_task = self.__task.get_next_task()
        if next_task is not None:
            self.__task.exit()
            task = next_task
            self.__task = task
            self.__map_manager.game_system.reset_timer()
            task.start()
            print("task:" + task.__class__.__name__)

        if isinstance(next_task, SceneToTitle):
            self.__next_scene = SceneTitle()

    def draw(self):
        self.__task.draw()

        game_info = super().game_info
        game_system = super().game_system

        if game_info.welcome_view_time > 0:
            game_info.decrement_welcome_view_time()
            welcome_text = "Welcome to floor {}.".format(game_info.floor)
            game_system.add_draw_object(
                Text(
                    welcome_text,
                    (300, 180),
                    Color.CYAN
                )
            )
        speed_text = "[S]peed "+str(game_system.speed)
        game_system.add_draw_object(
            Text(
                speed_text,
                (740, 40),
                Color.WHITE,
                Text.FontSize.SMALL
            )
        )

    def exit(self):
        print("title end")

    def get_next_scene(self):
        return self.__next_scene
