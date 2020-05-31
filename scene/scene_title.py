from scene.scene import Scene
from task.title.initialize import Initialize
from task.title.scene_to_map import SceneToMap
from game.game_system import GameSystem
from game.game_info import GameInfo
from manager.title_manager import TitleManager
from manager.map_manager import MapManager
from task.map.initialize import Initialize as MapInitialize


class SceneTitle(Scene):

    def __init__(self,
                 game_system: GameSystem,
                 game_info: GameInfo):
        title_manager = TitleManager(game_system, game_info)
        task = Initialize(title_manager)
        super().__init__(game_system, game_info, task)
        self.__next_scene: Scene = None

    def start(self):
        super().start()

    def update(self):
        super().update()

        from scene.scene_map import SceneMap
        if isinstance(super().task, SceneToMap):
            task = MapInitialize(
                super().game_system,
                super().game_info,
                MapManager()
            )
            self.__next_scene = SceneMap(
                super().game_system,
                super().game_info,
                task
            )

    def draw(self):
        super().draw()

    def exit(self):
        super().exit()

    def get_next_scene(self):
        return self.__next_scene
