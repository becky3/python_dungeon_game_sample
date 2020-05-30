
from game.game_system import GameSystem
from game.game_info import GameInfo
from scene.scene import Scene
from task.task import Task
from task.map.scene_to_title import SceneToTitle


class SceneMap(Scene):

    def __init__(self,
                 game_system: GameSystem,
                 game_info: GameInfo,
                 task: Task
                 ):
        super().__init__(
            game_system,
            game_info,
            task
        )
        self.__next_scene = None

    def start(self):
        pass

    def update(self):
        super().update()

        from scene.scene_title import SceneTitle
        if isinstance(super().task, SceneToTitle):
            self.__next_scene = SceneTitle(
                self.game_system,
                self.game_info
            )

    def draw(self):
        super().draw()

    def exit(self):
        super().exit()

    def get_next_scene(self):
        return self.__next_scene
