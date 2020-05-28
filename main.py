import sys

from game.game_system import GameSystem
from game.game_info import GameInfo
from manager.input_manager import InputManager
from scene.scene import Scene
from scene.scene_title import SceneTitle

__SCREEN_SIZE = (144, 144)
__POWER = 5
__MAP_CHIP_SIZE = (16, 16)


def main():

    game_system = GameSystem()
    game_system.set_caption("One hour Dungeon")
    game_system.setup_display(
        __SCREEN_SIZE,
        __POWER
    )

    game_info = GameInfo(
        __MAP_CHIP_SIZE,
        (
            int(__SCREEN_SIZE[0] / __MAP_CHIP_SIZE[0]),
            int(__SCREEN_SIZE[1] / __MAP_CHIP_SIZE[1]),
        )
    )

    scene: Scene = SceneTitle()
    scene.initialize(game_system, game_info)
    scene.start()

    while True:

        InputManager.updateEvents()

        if InputManager.isQuit():
            game_system.quit()
            sys.exit()

        game_system.progress()
        scene.update()
        next_scene = scene.get_next_scene()
        if next_scene is not None:
            scene.exit()
            scene = next_scene
            scene.initialize(game_system, game_info)
            scene.start()
            print("scene:" + scene.__class__.__name__)
            game_system.reset_timer()
            continue

        scene.draw()
        game_system.update_display()


if __name__ == '__main__':
    main()
