from typing import Optional

from model.event.enemy import Enemy
from manager.map_manager import MapManager
from manager.sound_manager import SE
from task.task import Task


class Battle(Task):

    def __init__(self, map_manager: MapManager, enemy: Enemy):
        self.__map_manager = map_manager
        self.__enemy = enemy
        self.__next_task = None

    def start(self):
        pass

    def update(self):

        mm = self.__map_manager
        event_manager = mm.event_manager
        player = mm.player
        game_system = mm.game_system

        enemy = self.__enemy

        enemy.battle()

        if enemy.stats.is_die():
            game_system.play_se(SE.ENEMY_DOWN)
            item = enemy.get_item()
            event_manager.remove_enemy(enemy)

            if item is not None:
                from task.map.get_item import GetItem
                self.__next_task = GetItem(mm, item)
                return

            if player.is_level_up(enemy):
                from task.map.level_up import LevelUp
                self.__next_task = LevelUp(mm)
                return
        else:
            game_system.play_se(SE.ATTACK)
            player.battle(enemy)
            player.back()

            if player.stats.is_die():
                from task.map.game_over import GameOver
                self.__next_task = GameOver(mm)
                return

        from task.map.wait_input import WaitInput
        self.__next_task = WaitInput(mm)

    def draw(self):
        mm = self.__map_manager
        mm.draw_map()
        mm.draw_parameter()
        mm.draw_floor_info()

    def exit(self):
        pass

    def get_next_task(self) -> Optional[Task]:
        return self.__next_task
